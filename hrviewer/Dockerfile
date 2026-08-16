# syntax=docker/dockerfile:1

# ---- Build stage: install deps into a target dir ----------------------------
# Debian 12 (bookworm) + Python 3.11 = ABI-kompatibel zum distroless-Runtime,
# damit die kompilierten .so (numpy/scipy/astropy/psycopg2) im finalen Image laden.
FROM python:3.11-slim-bookworm AS build

# binutils nur fuer `strip` im Build-Stage; landet NICHT im Runtime-Image.
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt .

# --target legt pure- und binary-Wheels in /packages ab; spaeter via PYTHONPATH.
RUN pip install --no-cache-dir --target=/packages -r requirements.txt

# Verhaltensneutrales Pruning: Debug-Symbole strippen + Bytecode-/Stub-Reste.
# Test-Verzeichnisse werden NICHT entfernt: numpy/scipy/astropy importieren
# Teile ihres tests-Pakets zur Laufzeit (z.B. numpy._core.tests._natype via
# numpy.testing, astropy.tests.runner im __init__).
# *.libs/ NICHT strippen: vendored OpenBLAS ist page-aligned gebaut, strip
# zerstoert das Alignment ("ELF load command not page-aligned").
RUN find /packages -name "*.so" -not -path "*.libs/*" -exec strip --strip-unneeded {} + 2>/dev/null || true \
    && find /packages -type d -name __pycache__ -prune -exec rm -rf {} + \
    && find /packages \( -name "*.pyc" -o -name "*.pyi" \) -delete

# ---- Runtime stage: distroless ---------------------------------------------
# python3-debian12 liefert Python 3.11, ca-certificates (fuer gdown-HTTPS und
# Postgres sslmode=require) und KEINE Shell -> kleines, gehaertetes Image.
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

# Abhaengigkeiten + nur die zur Laufzeit benoetigten Python-Module.
COPY --from=build /packages /packages
COPY run_pipeline.py gadgetbridge_migrate.py hrv_aggregate.py \
     spectral_bands_aggregate.py rr_quality.py ./

ENV PYTHONPATH=/packages \
    PYTHONUNBUFFERED=1

# Kein Shell-Form-ENTRYPOINT (distroless hat keine Shell) -> exec form.
ENTRYPOINT ["python", "/app/run_pipeline.py"]
