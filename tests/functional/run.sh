#!/bin/bash
ROOT_DIR="$(git rev-parse --show-toplevel)"
export PYTHONPATH="${ROOT_DIR}"

for test in ${ROOT_DIR}/tests/functional/suite/*; do
    OUTPUT="$(bash $test)"
    STATUS=$?
    if [ $STATUS -eq 0 ]; then
        echo "Pass: $test"
    else
        echo "Fail: $test"
        echo ""
        echo "$OUTPUT"
        exit -1
    fi
done
