#!/bin/bash


source $2
aws-profile $1

./scripts/readLog4J.sh dsservd $3 $4
