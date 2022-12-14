#!/bin/bash


source $2
aws-profile $1
./scripts/getLogFiles.sh dsservd $3 $4 $5
