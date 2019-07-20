#!/bin/bash -e

if [ -d test_repo ]; then
    echo "test_repo already exists, do nothing."
    exit 0
fi

git clone https://github.com/frostming/marko.git test_repo
