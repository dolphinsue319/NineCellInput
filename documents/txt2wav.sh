#!/bin/bash

echo -n "Enter the file name and press [ENTER]: "
read var_name
echo "The file name is: $var_name"
say -o $var_name.wav --data-format=I16@44100 -f $var_name.txt --channels=2
afplay $var_name.wav
