#!/usr/bin/env python
import os
import sys

from util.get_settings import load_settings

if __name__ == "__main__":
    load_settings(sys.argv)
    args = sys.argv
    if '--production' in args:
        args.remove('--production')

    from django.core.management import execute_from_command_line

    execute_from_command_line(args)
