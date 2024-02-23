#!/bin/bash

set -e
set -o pipefail

SOURCE_DIR="source"
OUT_DIR="dist"

dep_setup() {
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi

    source venv/bin/activate

    pip install --disable-pip-version-check --quiet --requirement requirements.txt
}

./run.sh dep-check 2>/dev/null || dep_setup

mkdir -p "${SOURCE_DIR}"
mkdir -p "${OUT_DIR}"
mapfile -t SOURCES < <(ls "${SOURCE_DIR}")

if [ "${#SOURCES[@]}" -eq 0 ]; then
    echo "Could not find question pools. Download docx version of question pools from https://ncvec.org/ and place in source directory." >&2
    exit 1
fi

for SOURCE in "${SOURCES[@]}"; do
    DB_NAME="${SOURCE%.*}.db"

    echo "Processing ${SOURCE}..." >&2

    ./run.sh parse "${SOURCE_DIR}/${SOURCE}" "${OUT_DIR}/${DB_NAME}"
done

echo "" >&2
echo "Processing complete. Check dist directory for output." >&2
