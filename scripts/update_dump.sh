#!/bin/bash
# Call with --nocalc if you want to skip recalculating cached variables

# Check pwd
if [ ! -f `pwd`/manage.py ]; then
    echo "You must run this from the root statsonice directory"
    exit
fi

# Get Settings
calculateVariables=1
for i in "$*" ; do
    if [ "$i" = "--nocalc" ]; then
        echo 'SKIPPING RECALCULATION OF CACHED VARIABLES'
        echo 'If you have changed scores, you should recalculate cached variables'
        calculateVariables=0
    fi
done

if [ $calculateVariables = 1 ]; then
    echo "Checking for Duplicate Skaters"
    python scripts/old/duplicate_skater_check.py
    echo "Recalculating cached values"
    python scripts/recalculate_cached_variables.py
fi

echo "Dumping database"
. util/keys/secret_key.sh
mysqldump --default-character-set=utf8 --user=$DB_USER --password=$DB_PASSWORD $DB_NAME > data/tmp.sql
python scripts/old/auth_dump.py data/tmp.sql data/db_dump_auth data/db_dump
rm data/tmp.sql

echo "Dumping database clearing script"
echo 'SET foreign_key_checks = 0;' > data/db_clear.sql
python manage.py sqlclear django_extensions >> data/db_clear.sql
python manage.py sqlclear south >> data/db_clear.sql
python manage.py sqlclear statsonice >> data/db_clear.sql
python manage.py sqlclear data_scraping >> data/db_clear.sql
echo 'BEGIN;' >> data/db_clear.sql
echo 'DROP TABLE `django_admin_log`;' >> data/db_clear.sql
echo 'DROP TABLE `django_content_type`;' >> data/db_clear.sql
echo 'DROP TABLE `django_session`;' >> data/db_clear.sql
echo 'DROP TABLE `django_site`;' >> data/db_clear.sql
echo 'COMMIT;' >> data/db_clear.sql
sed "s/DROP TABLE /DROP TABLE IF EXISTS /g" data/db_clear.sql > data/tmp.sql
sed '/ALTER TABLE/d' data/tmp.sql > data/db_clear.sql
rm data/tmp.sql

echo "Done"


