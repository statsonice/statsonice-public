Stats On Ice - Public
==========

This repository is a partial mirror of my StatsOnIce private repository.  It is manually 
updated from time to time - it is not a realtime reflection of the private repository.  
It therefore doesn't contain all the commits and branches that are used in development.  

There are also several missing directories:
- data - holds sql dumps and various other data in text format
- data\_scraping - holds code that scrapes and parses skating results into the database
- statsonice/migrations - Holds migration files created by Django South
- statsonice/static/bootstrap - Holds Twitter bootstrap static files

If you wish to view the hold codebase and maybe contribute, contact @albertyw

Dependencies
------------
System (`sudo apt-get install`)
- mysql-server
- pdftohtml
- memcached
- python-mysqldb
- python
- python-pip
- python libraries: run `pip install -r requirements.txt`

For the production server:
- Apache2 supporting mod\_wsgi

Installation Instructions
-------------------------

1.  Install Dependencies - remember your mysql root password
2.  Git clone this repository, make sure you are on the master branch
3.  `cd util` and run `git clone git@github.com:albertyw/statsonice-keys.git keys`
4.  Copy DB\_PASSWORD from `util/keys/secret_key.py` into `data/init_database.sql`
    and run `mysql -u root --password < data/init_database.sql`.  Run
    `git checkout data/init_database.sql` afterwards to remove the changes.
5.  Run `scripts/sync_db.sh --auth`
6.  Launch the server by running `scripts/runserver.sh`
7.  Check that everything is running by going to localhost:9001

Development Workflow
--------------------
After you have gotten everything installed

1.  Find issues to work on in github, assign them to yourself.
2.  Modify code, remember to `git pull` and `scripts/sync_db.sh` from time to time.
3.  `git status` and `git commit` your modified code.
4.  If your code is ready to be published, `git checkout production`,
`git merge [your current branch]`, `git push`, `git checkout master`.  Your new
code should be online in a minute.

Database Update Workflow
------------------------
When you update your database to fix information, you should commit your changes
to the repository so that your changes will be reflected on statsonice.com

1.  Update your database with corrected information.  There are many ways to
do this:
    - Use a SQL shell (`python manage.py dbshell`)
    - Use a Django shell (`python manage.py shell`)
    - Use the Django administration interface (http://localhost:port/admin)
    - Edit the sql `data/db_dump.sql` file *not recommended*
    - Run the data parsing scripts
2.  Check to make sure your data is correct.
3.  Run `update_dump.sh` in the `scripts` directory.
4.  Commit (`git commit data/db_dump.sql`) and push the updated database dump.

Scripts
-------
There are several scripts in the `scripts` directory that automate common tasks.
- `deploy.sh` - Runs on the production server to update it when there are new commits
- `memcached_status.sh` - Continuously shows the current status of memcached
- `recalculate_cached_variables.py` - Recalculate and save certain variables that
were calculated in the database
- `remove_temp_files.sh` - Remove backup and .pyc files from your repo
- `runserver.sh` - Convenience script that automatically restart the django server when
it crashes
- `sync_db.sh` - Update your database with the repository database dump
- `update_dump.sh` - Dumps the current database to the `data/db_dump.sql` file
- `update_memcached.py` - Updates memcached with data from database
- `old/assign_cities_to_coutries.py` - Assign city rows in database to countries
- `old/auth_dump.py` - Dump the auth tables from the database
- `old/combine_skaters.py` - Find and combine duplicate skaters
- `old/remove_skater_name_periods.py` - Change skater names to not have periods




[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/statsonice/statsonice-public/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

