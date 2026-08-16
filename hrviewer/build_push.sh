#!/usr/bin/env bash
# Baut das distroless-Image der HRV-Pipeline und pusht es in die Artifact
# Registry. Nach Code-Aenderungen an den .py-Dateien einfach erneut ausfuehren.
#
#   bash build_push.sh            # build + smoke-test + push
#   bash build_push.sh --no-push  # nur build + smoke-test (lokal)
#
# Voraussetzung: `docker login` zur Registry ist bereits erfolgt.
set -euo pipefail

IMG="us-central1-docker.pkg.dev/xy-archive-01/docker-default/hrv-pipeline:latest"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$HERE"

echo ">>> Build (single-manifest, ohne Attestation/SBOM, amd64) ..."
docker build \
  --platform linux/amd64 \
  --provenance=false --sbom=false \
  -t "$IMG" .

echo ">>> Smoke-Test: kompilierte + lokale Module im distroless-Image laden ..."
docker run --rm --entrypoint python "$IMG" -c "
import numpy, scipy, psycopg2, gdown
from astropy.timeseries import LombScargle
from scipy.signal import welch, hilbert, butter, filtfilt, csd
from scipy.interpolate import CubicSpline
import rr_quality
print('imports OK', numpy.__version__, scipy.__version__)
"

if [[ "${1:-}" == "--no-push" ]]; then
  echo ">>> --no-push gesetzt: Push uebersprungen."
  exit 0
fi

echo ">>> Push -> $IMG"
docker push "$IMG"

echo ">>> Fertig. Im Cloud Run Job ggf. 'Edit & deploy new revision' -> neueste Image-Digest waehlen."
