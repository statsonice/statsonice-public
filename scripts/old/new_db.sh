#!/bin/bash

# This creates a new database with only bare data

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

# Check the models
echo 'Validating models'
echo ''
python manage.py validate $settings
OUT=$?
if [ $OUT -ne 0 ];then
   exit
fi

# Clear the database
echo ''
echo 'CLEARING DATABASE'
echo ''
python manage.py reset_db -R default --noinput $settings
/bin/bash scripts/remove_temp_files.sh

# Make the database
echo ''
echo 'CREATING DATABASE'
echo ''
python manage.py syncdb --noinput $settings

# Add Super Users
echo ''
echo 'ADDING SUPER USERS'
echo ''
python scripts/create_super_user.py $settings

# Prepopulate Enum fields
echo ''
echo 'PRE POPULATING DATABASE TABLES'
echo ''
python scripts/old/prepopulate_data.py $settings
