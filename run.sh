#!/bin/bash

export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)/src:$PYTHONPATH"

exec python3 -u -m examdb.cli."$1" "${@:2}"
