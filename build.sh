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

mapfile -t SOURCES < <(ls "${SOURCE_DIR}")
mkdir -p "${OUT_DIR}"

for SOURCE in "${SOURCES[@]}"; do
    DB_NAME="${SOURCE%.*}.db"

    echo "Processing ${SOURCE}..."

    ./run.sh parse "${SOURCE_DIR}/${SOURCE}" "${OUT_DIR}/${DB_NAME}"
done
