#!/bin/bash

# This wipes the development database and repopulates it

# Check pwd
if [ ! -f `pwd`/manage.py ]; then
    echo "You must run this from the root statsonice directory"
    exit
fi

# Get Settings
auth=0
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
cat data/db_dump.*.sql | mysql --default-character-set=utf8 --user=$DB_USER --password=$DB_PASSWORD $DB_NAME
if [[ $auth == 1 ]] ; then
    cat data/db_dump_auth.*.sql | mysql --default-character-set=utf8 --user=$DB_USER --password=$DB_PASSWORD $DB_NAME
fi

# Clearing memcached
echo 'CLEARING MEMCACHED'
if [[ $DB_NAME == 'statsonice' ]]; then
    echo 'flush_all' | nc localhost 11211
else
    echo 'flush_all' | nc localhost 11212
fi

# Running variable caching script
echo 'STARTING MEMCACHED UPDATER'
screen -d -m python scripts/update_memcached.py
