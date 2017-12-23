set -x

SERVICE_NAME="word-count-service"
SERVICE_BUCKET="nhardi-mrkirm2-$SERVICE_NAME"

SCRIPT="word_count_script.py"
SCRIPT_PATH="$TEST_DATA/$SCRIPT"
SCRIPT_URL="https://s3.eu-central-1.amazonaws.com/$SERVICE_BUCKET/apps/SCRIPT"

INPUT="sample_input.txt"
INPUT_PATH="$TEST_DATA/$INPUT"

function stop_service()
{
    python -m nebo service --stop --instance "$INSTANCE_ID"
}

function cleanup()
{
    stop_service
    # remove buckets
}

function die()
{
    msg="$1"
    echo "$msg"

    cleanup
    exit 1
}

function start_service()
{
    INSTANCE_ID=$(python -m nebo service --start -q --name "$SERVICE_NAME" --script "$SCRIPT_PATH")
}

function issue_request()
{
    OUTPUT_URL=$(python -m nebo run --service="$SERVICE_NAME" --input-file="$INPUT_PATH")
}

function check_result()
{
    curl -s "$OUTPUT_URL" | jq -e .hello
}

start_service || die "can't start the service"
issue_request || die "request failed"
check_result  || die "result check failed"
cleanup

exit 0
