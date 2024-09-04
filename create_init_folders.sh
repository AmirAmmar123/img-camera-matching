#!/bin/bash
if [ $# -lt 1 ]; then
    echo "error: <usage>: ./create_init_folders <target-directory1> <target-directory2> ..."
    exit 1
fi

for dir in "$@"; do
    if [ -e "Data-Base/$dir" ]; then
        echo "Path exists: Data-Base/$dir"
    else
        echo "Path does not exist: Data-Base/$dir"
        echo "Creating new path at Data-Base/$dir"
        mkdir  Data-Base/$dir
    fi


    mkdir -p Data-Base/$dir/{pnu_id,testing,training}./
    echo "Folders created successfully at Data-Base/$dir"
    tree Data-Base/$dir
done
