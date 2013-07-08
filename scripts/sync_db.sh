#!/bin/bash

# This wipes the development database and repopulates it

# Check pwd
if [ ! -f `pwd`/manage.py ]; then
    echo "You must run this from the root statsonice directory"
    exit
fi

# Get Settings
for i in "$*" ; do
    if [ "$i" = "--auth" ]; then
        echo 'LOADING AUTH TABLES'
        auth=1
    fi
done

# Check the models
echo 'Validating models'
echo ''
python manage.py validate
OUT=$?
if [ $OUT -ne 0 ];then
   exit
fi


. util/keys/secret_key.sh
# Clear the database
echo 'DATABASE: '$DB_NAME
echo 'CLEARING DATABASE'
if [[ $auth == 1 ]] ; then
    python manage.py reset_db --router=default --noinput
else
    mysql --default-character-set=utf8 --user=$DB_USER --password=$DB_PASSWORD $DB_NAME < data/db_clear.sql
fi

# Make the database
echo 'CREATING AND POPULATING DATABASE'
mysql --default-character-set=utf8 --user=$DB_USER --password=$DB_PASSWORD $DB_NAME < data/db_dump.sql
if [[ $auth == 1 ]] ; then
    mysql --default-character-set=utf8 --user=$DB_USER --password=$DB_PASSWORD $DB_NAME < data/db_dump_auth.sql
fi

# Clearing memcached
echo 'CLEARING MEMCACHED'
echo 'flush_all' | nc localhost 11211