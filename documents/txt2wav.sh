#!/bin/bash

echo -n "Enter the file name and press [ENTER]: "
read var_name
echo "The file name is: $var_name"
say -o $var_name.wav --data-format=UI8@8000 -f $var_name.txt
afplay $var_name.wav
