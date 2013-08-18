#!/bin/bash
# This script gives status on memcached
. util/keys/secret_key.sh
if [[ $DB_NAME == 'statsonice' ]]; then
    watch "echo stats | nc 127.0.0.1 11211"
else
    watch "echo stats | nc 127.0.0.1 11212"
fi
