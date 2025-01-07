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

# create the data-base/results directory if it does not exist
if [ ! -d "data-base/results" ]; then
    echo "creating data-base/results/..."
    mkdir -p data-base/results
    echo "done"
fi
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

if [ -e "all_results/results" ]; then
    echo "Path exists: all_results/results"
else
    echo "Path does not exist: all_results/results"
    echo "Creating new path at all_results/results"
    mkdir -p all_results/results
fi


# create the logging directory if it does not exist
if [ ! -d "logging" ]; then
    echo "creating logging/..."
    mkdir -p logging
    echo "done"
fi