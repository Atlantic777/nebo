set -x

SERVICE_NAME="word-count-service"
DEFAULT_BUCKET="nhardi-mrkirm2-$SERVICE_NAME"
DEFAULT_SCRIPT="word_count_script.py"
DEFAULT_URL="https://s3.eu-central-1.amazonaws.com/$DEFAULT_BUCKET/apps/$DEFAULT_SCRIPT"
INPUT="sample_input.txt"
OUTPUT="$INPUT"

function stop_service()
{
    python -m nebo service --stop --instance="$INSTANCE_ID"
}

function die()
{
    msg="$1"
    echo "$msg"
    stop_service
    exit 1
}

function start_service()
{
    INSTANCE_ID=$(python -m nebo service --start -q --name=test-service --script="$TEST_DATA/$DEFAULT_SCRIPT" --name="$SERVICE_NAME")
}

function issue_request()
{
    python -m nebo run --service="$SERVICE_NAME" --input-file="$TEST_DATA/$INPUT" --args="hello,world"
}

function check_input()
{
    aws s3 ls s3://$DEFAULT_BUCKET/inputs/ | grep -i "$INPUT"
}

function check_output()
{
    aws s3 ls s3://$DEFAULT_BUCKET/outputs/ | grep -i "$OUTPUT"
}

start_service || die "can't start the service"
issue_request || die "can't issue the request"
check_input   || die "can't find the input file"
check_output  || die "can't find the output file"
sleep 180s
check_input   && die "the input file is still there"
check_output  && die "the output file is still there"
stop_service  || die "can't stop the service"
exit 0
