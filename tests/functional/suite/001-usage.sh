OUTPUT="$(python -m nebo; python -m nebo service --help; python -m nebo run --help)"

function check()
{
    TERM=$1
    echo "$OUTPUT" | grep -i $TERM || exit 1
}

check "usage"
check "service"
check "run"
check "\-\-name"
check "\-\-list"
