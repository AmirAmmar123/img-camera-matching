#!/bin/bash

# Check if the correct number of arguments are passed
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_dir> <target_dir>"
    exit 1
fi

# Assign arguments to variables
source_dir="$1"
target_dir="$2"

# Define destination directories
testing_dir="$target_dir/testing"
training_dir="$target_dir/training"

# Check if testing and training directories exist
if [ ! -d "$testing_dir" ] || [ ! -d "$training_dir" ]; then
    echo "Error: Either the testing or training directory does not exist."
    exit 1
fi

# Move 100 random images to the testing directory
find "$source_dir" -type f | shuf -n 100 | while read file; do
    mv "$file" "$testing_dir/"
done

# Move the remaining images to the training directory
find "$source_dir" -type f | while read file; do
    mv "$file" "$training_dir/"
done

echo "Images moved successfully."
