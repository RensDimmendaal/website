#!/bin/bash

# check if in correct directory
if [[ ! "$(basename $(pwd))" == "website" ]]; then
    echo "Please run this script from the website directory"
    exit 1
fi

if [ -d "plash-dir" ]; then
    trash plash-dir
fi

mkdir -p plash-dir

cp -r posts plash-dir/

# Set PLASH_APP_ID based on dev flag
if [ "$1" == "rens-"* ]; then
    echo "export PLASH_APP_ID="$1" >> plash-dir/.plash
else
    echo "export PLASH_APP_ID="rensdimmendaal.com" >> plash-dir/.plash
fi

cp main.py plash-dir/
cp requirements.txt plash-dir/

plash_deploy --path plash-dir
