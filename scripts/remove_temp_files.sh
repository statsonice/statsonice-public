#!/bin/bash

# This removes temporary editing files from the code
if [ ! -f `pwd`/manage.py ]; then
    echo "You must run this from the root statsonice directory"
    exit
fi

find . -name "*.pyo" | xargs rm -v
find . -name "*.pyc" | xargs rm -v
find . -name "*~" | xargs rm -v
