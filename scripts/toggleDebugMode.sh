#!/bin/bash


instanceID=$2
file=$3
mode=$4

# Load the common ssh setup
COMMAND_NAME="ssh"
source ./scripts/aws-ssh-common.sh

if [ $mode == "OFF" ]
then
  ssh -i $EC2_SSH_KEY -o StrictHostKeyChecking=no dsservd@$instanceID  " sed -i \"/Root/,+0 s/DEBUG/ERROR/\" $file ; sed -i \"/DSLog/,+0 s/DEBUG/ERROR/\" $file ;sed -i \"/server.log/,+2 s/DEBUG/ERROR/\" $file"
elif [ $mode == "ON" ]
then
  ssh -i $EC2_SSH_KEY -o StrictHostKeyChecking=no dsservd@$instanceID  " sed -i \"/Root/,+0 s/ERROR/DEBUG/\" $file ; sed -i \"/DSLog/,+0 s/ERROR/DEBUG/\" $file ;sed -i \"/server.log/,+2 s/ERROR/DEBUG/\" $file"
fi