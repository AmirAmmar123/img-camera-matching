#!/bin/bash
if [ $# -lt 1 ]; then
    echo "error: <usage>: ./create_init_folders <target-directory1> <target-directory2> ..."
    exit 1
fi

if [ ! -e "plots/" ]; then
        echo "creating plots/..."
        mkdir plots/
        echo "done"
        echo "creating plots/gaussian..."
        mkdir plots/gaussian
        echo "done"
         echo "creating plots/gaussian/theoretical..."
        mkdir plots/gaussian/theoretical
        echo 'done'
        echo "creating plots/pnu_hist..."
        mkdir "plots/pnu_hist"
        echo "done"
        tree plots
fi 

for dir in "$@"; do
    


    if [ -e "data-base/$dir" ]; then
        echo "Path exists: Data-Base/$dir"
    else
        echo "Path does not exist: data-base/$dir"
        echo "Creating new path at data-base/$dir"
        mkdir  data-base/$dir
    fi


    mkdir -p data-base/$dir/{pnu_id,testing,training}/
    echo "Folders created successfully at data-base/$dir"
    tree data-base/$dir
done
