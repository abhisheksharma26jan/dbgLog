#!/bin/bash


instanceID=$2
file=$3
searchKey=$4
# Load the common ssh setup
COMMAND_NAME="ssh"
source ./scripts/aws-ssh-common.sh

echo $EC2_SSH_KEY


ssh -i $EC2_SSH_KEY -oStrictHostKeyChecking=no dsservd@$instanceID bash -c "' find logs/ '"
