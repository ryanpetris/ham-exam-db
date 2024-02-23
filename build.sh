#!/bin/bash

set -e
set -o pipefail

SOURCE_DIR="source"
OUT_DIR="dist"

mapfile -t SOURCES < <(ls "${SOURCE_DIR}")
mkdir -p "${OUT_DIR}"

for SOURCE in "${SOURCES[@]}"; do
    DB_NAME="${SOURCE%.*}.db"

    echo "Processing ${SOURCE}..."

    ./examdb-parse.sh "${SOURCE_DIR}/${SOURCE}" "${OUT_DIR}/${DB_NAME}"
done
