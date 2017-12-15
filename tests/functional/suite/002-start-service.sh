output=""

function die()
{
    exit 1
}

function check()
{
    cmd=$1
    output="$($cmd 2>&1)"
    ok=$?
    return $ok
}

function check_true()
{
    check "$1" || ( echo -e "Command: $1\n\n" "$output\n\n" && die )
}

function check_false()
{
    ! check "$1" || ( echo -e "Should fail!\n Command: $1\n\n" "$output\n\n" && die )
}

# regular start
check_true "python -m nebo service --start -q --script=$TEST_DATA/service_script.py"

# regular stop
check_true "python -m nebo service --stop --instance=$output"

# # incomplete start
check_false "python -m nebo service --start"  

# # incomplete stop
check_false "python -m nebo service --stop"

# # if you are here, all tests passed
exit 0
