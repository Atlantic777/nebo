output=""

function die()
{
    msg="$1"
    echo -e "$msg"
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
    check "$1" || die "Command: $1\n\n" "$output\n\n"
}

function check_false()
{
    ! check "$1" || die "Should fail!\n Command: $1\n\n" "$output\n\n"
}

# regular start
check_true "python -m nebo service --start -q --script=$TEST_DATA/dummy_script.py --name=test-service"

# regular stop
check_true "python -m nebo service --stop --instance=$output"

# incomplete start
check_false "python -m nebo service --start"  

# incomplete stop
check_false "python -m nebo service --stop"

# if you are here, all tests passed
exit 0
