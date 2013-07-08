#!/bin/bash
# This script handles deploying the new code on the production server
# This should only be run on the production server

branch=$1
if [[ $branch == "production" ]] ; then
    basedir='/home/statsonice_production/'
elif [[ $branch == "master" ]] ; then
    basedir='/home/statsonice_staging/'
else
    echo 'No branch selected'
    exit
fi
force="false"
if [[ $2 == "force" ]] ; then
    force="force"
fi

cd $basedir
git checkout $branch
echo 'On branch '$branch

# Check if there are code updates
echo "Fetching new code"
git fetch origin
reslog=$(git log HEAD..origin/$branch --stat)
echo "$reslog"
if [ "${reslog}" == "" ] && [ "$force" != "force" ] ; then
    echo "No new code to deploy"
    exit 0
fi
echo "Found new code"

# Wait for previous deployments to finish
while [ -f $basedir/maintenance.txt ] ;
do
    echo "Waiting for previous deployments to finish"
    sleep 10
done

# Deploy
echo "Putting site in maintenance mode"
touch $basedir/maintenance.txt
echo "Removing left-over temporary files"
/bin/bash $basedir/scripts/remove_temp_files.sh > /dev/null 2>&1
echo "Pulling new code"
git pull
if [[ "$reslog" == *db_dump* ]] || [[ "$force" == "force" ]] ; then
    echo "Synchronizing Database"
    /bin/bash $basedir/scripts/sync_db.sh
    echo "Database Synchronized"
else
    echo "No database updates found; not synchronizing database"
fi

# Update blog cache
echo "Updating blog cache"
curl http://www.statsonice.com/cache_blog/ > /dev/null

# Remove maintence mode file
echo "Re-enabling site"
rm $basedir/maintenance.txt
