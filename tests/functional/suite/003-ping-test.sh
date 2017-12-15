set -x
SERVICE_SCRIPT="$DEST_DATA/dummy_service.py"
INIT_SCRIPT="$TEST_DATA/dummy_init.sh"

function die
{
    exit 1
}

# start service
INSTANCE_ID=$(python -m nebo service --start -q --script="$SERVICE_SCRIPT" --init="$INIT_SCRIPT")
test $? || die

# aws describe
description=$(aws ec2 describe-instances --instance-ids="$INSTANCE_ID")
test $? || die

# jq extract public ip
IP_ADDR=$(echo "$description" | jq -r .Reservations[].Instances[].PublicIpAddress)
test $? || die

# ping ip
ping -W 1 -c 3 $IP_ADDR || die

# stop service
python -m nebo service --stop --instance "$INSTANCE_ID" || die
