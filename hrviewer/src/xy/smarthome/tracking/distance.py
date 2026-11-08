"""Signal strength to distance approximation."""
from __future__ import annotations
import math
_FREQ_MHZ = {False: 2437, True: 5500}

def estimate_distance(percent: int | None, is_5ghz: bool, tx_dbm: float, exponent: float) -> tuple[float | None, bool]:
    """Log-distance path loss model.

    ``percent`` is mapped linearly to -100..-50 dBm. Returns ``(metres,
    saturated)``; a saturated reading (100 %) is only an upper bound.
    """
    if not isinstance(percent, int) or percent <= 0:
        return (None, False)
    rssi_dbm = percent / 2 - 100
    loss_1m = 20 * math.log10(_FREQ_MHZ[is_5ghz]) - 27.55
    metres = 10 ** ((tx_dbm - loss_1m - rssi_dbm) / (10 * exponent))
    return (metres, percent >= 100)