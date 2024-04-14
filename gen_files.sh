#!/bin/bash

# Check if the number of files is provided as an argument
if [ $# -eq 0 ]; then
  echo "Please provide the number of files as a command line argument."
  exit 1
fi

num_files=$1

for ((i=1; i<=num_files; i++)); do
  # Generate a random 64-byte hexadecimal filename
  filename=$(head -c 32 /dev/urandom | xxd -p -c 32)
  
  # Extract the first 3 characters of the filename
  dir1=${filename:0:1}
  dir2=${filename:1:1}
  dir3=${filename:2:1}
  
  # Create the nested directories if they don't exist
  mkdir -p "/tmp/test/$dir1/$dir2/$dir3"
  
  # Create an empty file with the random filename in the nested directory
  touch "/tmp/test/$dir1/$dir2/$dir3/$filename"
done







