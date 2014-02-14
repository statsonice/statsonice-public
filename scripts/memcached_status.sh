#!/bin/bash
# This script gives status on memcached
watch "echo stats | nc 127.0.0.1 11211"
