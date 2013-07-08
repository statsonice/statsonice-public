#!/bin/bash

# a simple script to remove temp files and restart the server

# Check pwd
if [ ! -f `pwd`/manage.py ]; then
    echo "You must run this from the root statsonice directory"
    exit
fi


# Get Settings
settings='--settings=util.test_settings'
for i in "$*" ; do
    if [ "$i" = "--production" ]; then
        echo 'USING PRODUCTION SETTINGS'
        settings='--settings=util.settings'
    fi
done

python manage.py runserver 0.0.0.0:9001 $settings
sleep 2s
/bin/bash scripts/runserver.sh "$@"
