OUTPUT="$(python -m nebo)"

function check()
{
    TERM=$1
    echo "$OUTPUT" | grep -i $TERM || exit 1
}

check "usage"
check "service"
check "run"
