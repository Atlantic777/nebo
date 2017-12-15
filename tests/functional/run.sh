#!/bin/bash
export ROOT_DIR="$(git rev-parse --show-toplevel)"
export PYTHONPATH="${ROOT_DIR}"
export TEST_DATA="$ROOT_DIR/tests/data"

filter=$1

for test in ${ROOT_DIR}/tests/functional/suite/*; do
    if $(echo $test | grep "$filter" > /dev/null); then
        OUTPUT="$(bash $test 2>&1)"
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
            echo "Pass: $test"
        else
            echo "Fail: $test"
            echo ""
            echo "$OUTPUT"
            exit 1
        fi
    fi
done
