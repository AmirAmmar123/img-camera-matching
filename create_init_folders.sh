#!/bin/bash
if [ ! $# -eq 1 ]; then
    echo "error: <usage>: ./create_init_folders <target-path>"
    exit 1 
fi


if [ -e "Data-Base/$1" ]; then
    echo "Path exists: Data-Base/$1"
else
    echo "Path does not exist: Data-Base/$1"
    echo "Creating new path at Data-Base/$1"
    mkdir  Data-Base/$1
fi


mkdir -p Data-Base/$1/{pnu_id,testing,training}
echo "Folders created successfully at Data-Base/$1"
tree Data-Base/$1