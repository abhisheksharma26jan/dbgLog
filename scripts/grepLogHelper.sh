#!/bin/bash


source $2
aws-profile $1
./scripts/grepLog.sh dsservd $3 $4 $5 $6 $7
