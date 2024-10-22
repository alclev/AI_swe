#!/bin/bash

# Directory to walk through
DIR="$(pwd)"

# Directories to exclude (add any directories you want to exclude here)
EXCLUDE_DIRS=("__pycache__" ".venv" "tmp")

# Function to check if a directory is in the exclusion list
is_excluded() {
    for exclude in "${EXCLUDE_DIRS[@]}"; do
        if [[ "$1" == *"$exclude"* ]]; then
            return 0
        fi
    done
    return 1
}

# Function to dump file content
dump_files() {
    for file in "$1"/*; do
        if [ -d "$file" ]; then
            # Check if the directory is excluded
            if ! is_excluded "$file"; then
                dump_files "$file"
            fi
        elif [ -f "$file" ]; then
            echo "Contents of $file:"
            cat "$file"
            echo ""
        fi
    done
}

# Start the directory walk
dump_files "$DIR"
