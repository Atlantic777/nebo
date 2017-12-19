DEFAULT_BUCKET="nhardi-mrkirm2-scripts"
DEFAULT_SCRIPT="dummy_script.py"
DEFAULT_URL="https://$DEFAULT_BUCKET.s3.amazonaws.com/$DEFAULT_SCRIPT"

function remove_bucket()
{
    aws s3 rb --force "s3://$DEFAULT_BUCKET" &>/dev/null
}

function check_bucket()
{
    aws s3 ls "s3://$DEFAULT_BUCKET" &>/dev/null
}

function check_file()
{
    aws s3 ls "s3://$DEFAULT_BUCKET" &>/dev/null
}

function create_service()
{
    INSTANCE_ID=$(python -m nebo service --start -q --script="$TEST_DATA/$DEFAULT_SCRIPT")
}

function kill_service()
{
    python -m nebo service --stop --instance="$INSTANCE_ID"
}


function die()
{
    msg="$1"
    remove_bucket

    echo "$msg"
    exit 1
}

# setup: remove bucket if needed
remove_bucket

check_bucket                                     && die "Bucket already there!"
create_service                                   || die "service setup failed"
check_bucket                                     || die "Default bucket not there."
check_file                                       || die "Dummy script not uploaded."
wget --quiet "$DEFAULT_URL" -O /dev/null         || die "Can't reach the script with wget."
kill_service                                     || die "Can't kill the service."
check_bucket                                     && die "Bucket still present"

# if you are here, all tests passed
exit 0
