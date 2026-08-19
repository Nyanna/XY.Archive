"""Backend-neutral Arrow result + IPC serialisation -- built on *nanoarrow*.

This module replaces the previous PyArrow dependency. It offers two things:

* :func:`stream_to_ipc` -- serialise *anything* that exposes the Arrow C stream
  interface (``__arrow_c_stream__``) straight to an Arrow IPC stream. DuckDB
  relations implement that interface natively and export their data zero-copy,
  so on the read path the query result is streamed to IPC bytes without ever
  materialising a heavyweight table -- this is the memory win over PyArrow.

* :class:`QueryResult` / :class:`ColumnsResult` -- a tiny value type the data
  access layer hands back to the HTTP layer. It serialises to the exact same
  Arrow IPC stream the browser's apache-arrow already consumes, or to a plain
  column dict for the ``format=json`` debug path.

The IPC bytes produced here are byte-compatible with what PyArrow used to emit
(standard Arrow *stream* format), so the frontend needs no change.
"""
from __future__ import annotations

import io
from typing import Mapping

import numpy as np
import nanoarrow as na
from nanoarrow import ipc

ARROW_MIME = "application/vnd.apache.arrow.stream"


# ---------------------------------------------------------------------------
# Low-level nanoarrow helpers
# ---------------------------------------------------------------------------
def stream_to_ipc(source) -> bytes:
    """Serialise an Arrow C stream source to a self-contained IPC stream.

    ``source`` is any object implementing ``__arrow_c_stream__`` (e.g. a DuckDB
    relation) or a nanoarrow array/stream. The stream is consumed chunk by
    chunk, so the full result never has to live in memory as one table.
    """
    out = io.BytesIO()
    with ipc.StreamWriter.from_writable(out) as writer:
        writer.write_stream(na.c_array_stream(source))
    return out.getvalue()


def _int64(values: np.ndarray):
    a = np.ascontiguousarray(values, dtype=np.int64)
    return na.c_array_from_buffers(na.int64(), len(a), [None, na.c_buffer(a)])


def _float64(values: np.ndarray):
    """Build a float64 Arrow array, mapping NaN -> Arrow null (validity map)."""
    a = np.ascontiguousarray(values, dtype=np.float64)
    n = len(a)
    isnull = np.isnan(a)
    if not isnull.any():
        return na.c_array_from_buffers(na.float64(), n, [None, na.c_buffer(a)])
    valid_bits = np.packbits((~isnull).astype(np.uint8), bitorder="little")
    vals = np.ascontiguousarray(np.where(isnull, 0.0, a), dtype=np.float64)
    return na.c_array_from_buffers(
        na.float64(),
        n,
        [na.c_buffer(valid_bits.tobytes()), na.c_buffer(vals)],
        null_count=int(isnull.sum()),
    )


def _column_array(values: np.ndarray):
    values = np.asarray(values)
    if np.issubdtype(values.dtype, np.integer) or values.dtype == np.bool_:
        return na.int64(), _int64(values)
    return na.float64(), _float64(values)


def columns_to_struct(columns: Mapping[str, np.ndarray]):
    """Build a single nanoarrow struct array from in-memory numpy columns."""
    fields: dict[str, object] = {}
    children = []
    n = 0
    for name, values in columns.items():
        dtype, child = _column_array(values)
        fields[name] = dtype
        children.append(child)
        n = child.length
    return na.c_array_from_buffers(na.struct(fields), n, [None], children=children)


# ---------------------------------------------------------------------------
# Result value types handed to the HTTP layer
# ---------------------------------------------------------------------------
class QueryResult:
    """A backend-neutral query result: Arrow IPC bytes or a column dict."""

    def to_ipc(self) -> bytes:  # pragma: no cover - interface
        raise NotImplementedError

    def to_pydict(self) -> dict[str, list]:  # pragma: no cover - interface
        raise NotImplementedError


class ColumnsResult(QueryResult):
    """Result backed by in-memory numpy columns (the fastparquet backend)."""

    def __init__(self, columns: Mapping[str, np.ndarray]):
        self._cols = {k: np.asarray(v) for k, v in columns.items()}

    def to_ipc(self) -> bytes:
        return stream_to_ipc(columns_to_struct(self._cols))

    def to_pydict(self) -> dict[str, list]:
        out: dict[str, list] = {}
        for name, values in self._cols.items():
            if np.issubdtype(values.dtype, np.floating):
                out[name] = [None if v != v else float(v) for v in values]
            elif values.dtype == np.bool_:
                out[name] = [int(v) for v in values]
            else:
                out[name] = [int(v) for v in values]
        return out
