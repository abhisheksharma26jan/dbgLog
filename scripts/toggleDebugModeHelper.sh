#!/bin/bash


source $2
aws-profile $1

./scripts/toggleDebugMode.sh dsservd $3 $4 $5
