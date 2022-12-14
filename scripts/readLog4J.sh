#!/bin/bash


instanceID=$2
file=$3

# Load the common ssh setup
COMMAND_NAME="ssh"
source ./scripts/aws-ssh-common.sh

ssh -i $EC2_SSH_KEY -o StrictHostKeyChecking=no dsservd@$instanceID bash -c "' cat $file '"
