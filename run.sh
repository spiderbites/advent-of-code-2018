#!/bin/bash

set -e

day=$1
part=$2
test=$3

if [[ -z "${test// }" ]]; then
  python3 $day.py $part ./inputs/$day.txt
else
  python3 $day.py $part ./inputs/$day"_test".txt
fi
