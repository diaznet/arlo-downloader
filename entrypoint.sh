#!/bin/bash

set -e

# Detect old configuration format where MEDIA_FOLDER contained both path and filename pattern
if [[ -n "$MEDIA_FOLDER" && "$MEDIA_FOLDER" == *'${'* ]]; then
    echo "============================================================"
    echo "ERROR: Breaking changes in this version!"
    echo ""
    echo "MEDIA_FOLDER no longer accepts filename patterns."
    echo "The configuration has been split into two variables:"
    echo ""
    echo "  MEDIA_FOLDER = base directory (e.g., /records)"
    echo "  FILENAME     = naming pattern (e.g., \${Y}/\${m}/\${F}T\${t}_\${N}_\${SN})"
    echo ""
    echo "Your current MEDIA_FOLDER contains substitution tokens:"
    echo "  MEDIA_FOLDER=$MEDIA_FOLDER"
    echo ""
    echo "Please update your configuration. See README for details."
    echo "============================================================"
    exit 1
fi

if [[ -z "$MEDIA_FOLDER" ]]; then
    MEDIA_FOLDER="/records"
fi

if [[ -z "$FILENAME" ]]; then
    FILENAME='${Y}/${m}/${F}T${t}_${N}_${SN}'
fi

exec python /arlo-downloader/arlo-downloader.py \
    --media-folder "$MEDIA_FOLDER" \
    --filename "$FILENAME" \
    --tfa-type "${TFA_TYPE:-PUSH}" \
    --tfa-source "${TFA_SOURCE:-push}" \
    --tfa-retries "${TFA_RETRIES:-10}" \
    --tfa-delay "${TFA_DELAY:-5}" \
    --tfa-host "${TFA_HOST:-_invalid}" \
    --tfa-username "${TFA_USERNAME:-###}" \
    --tfa-password "${TFA_PASSWORD:-###}"
