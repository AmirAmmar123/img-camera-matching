# This script initializes the folder structure for the img-camera-matching project.
# It creates necessary directories for plots, data-base, and all_results.
#
# Usage:
#   ./init.sh <target-directory1> <target-directory2> ...
#
# Arguments:
#   <target-directory1> <target-directory2> ... : List of target directories to be created under data-base and all_results.
#
# The script performs the following actions:
# 1. Checks if the required number of arguments are provided. If not, it displays an error message and exits.
# 2. Creates the "plots" directory and its subdirectories ("gaussian/theoretical" and "pnu_hist") if they do not exist.
# 3. For each target directory provided as an argument:
#    - Checks if the "data-base" directory exists. If not, it creates the directory.
#    - Checks if the target directory exists under "data-base". If not, it creates the directory and its subdirectories ("pnu_id", "testing", "training").
#    - Displays the created directory structure using the tree command.
# 4. Creates the "all_results" directory if it does not exist.
# 5. For each target directory provided as an argument:
#    - Checks if the target directory exists under "all_results". If not, it creates the directory.
#    - Displays the created directory structure using the tree command.
#!/bin/bash

HOME=~
PROJECT_DIR="$HOME/img-camera-matching"
DB_DIR="data-base"
PROJECT_FULL_PATH="$PROJECT_DIR/$DB_DIR"

if [ $# -lt 1 ]; then
    echo "error: <usage>: ./create_init_folders <target-directory1> <target-directory2> ..."
    exit 1
fi

# create the plot directory and sub directories if they do not exist
if [ ! -d "plots" ]; then
    echo "creating plots/..."
    mkdir -p plots/gaussian/theoretical plots/pnu_hist
    echo "done"
else
    if [ ! -d "plots/gaussian" ]; then
        echo "creating plots/gaussian..."
        mkdir -p plots/gaussian/theoretical
        echo "done"
    elif [ ! -d "plots/gaussian/theoretical" ]; then
        echo "creating plots/gaussian/theoretical..."
        mkdir -p plots/gaussian/theoretical
        echo "done"
    fi

    if [ ! -d "plots/pnu_hist" ]; then
        echo "creating plots/pnu_hist..."
        mkdir -p plots/pnu_hist
        echo "done"
    fi
fi


# create the data-base directory and sub directories if they do not exist
for dir in "$@"; do
    if [ -e $PROJECT_FULL_PATH ]; then
        echo "Path exists: $PROJECT_FULL_PATH"
    else
        echo "Path does not exist: $PROJECT_FULL_PATH"
        echo "Creating new path at $PROJECT_FULL_PATH"
        mkdir -p $PROJECT_FULL_PATH
    fi
    
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
# create the all_results directory and sub directories if they do not exist
if [ ! -d "all_results" ]; then
    echo "creating all_results/..."
    mkdir -p all_results
    echo "done"
fi

for dir in "$@"; do
    if [ -e "all_results/$dir" ]; then
        echo "Path exists: all_results/$dir"
    else
        echo "Path does not exist: all_results/$dir"
        echo "Creating new path at all_results/$dir"
        mkdir -p all_results/$dir
    fi
    echo "Folders created successfully at all_results/$dir"
    tree all_results/$dir
done