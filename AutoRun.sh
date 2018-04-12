#!/bin/bash

read -p "Save the data as: " filename
python IPMIPSUStatus_Script_User.py ${filename}
python Compared_Script.py ${filename}
