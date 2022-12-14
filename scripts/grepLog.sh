#!/bin/bash


instanceID=$2
file=$3
searchKey=$4
A=$5
B=$6
# Load the common ssh setup
COMMAND_NAME="ssh"
source ./scripts/aws-ssh-common.sh

#echo $EC2_SSH_KEY

ssh -i $EC2_SSH_KEY -o StrictHostKeyChecking=no dsservd@$instanceID bash -c "' grep -rin -A $A -B $B $searchKey $file '"
