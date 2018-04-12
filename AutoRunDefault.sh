#!/bin/bash

NOW=$(date +"%Y%m%d%H%M")
echo "Save the data as: $NOW "
python IPMIPSUStatus_Script.py $NOW
python Compared_Script.py $NOW