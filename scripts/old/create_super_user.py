#!/usr/bin/python
"""
This file creates super users in the django database
"""

import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)

from django.contrib.auth.models import User

superusers = ['albertyw', 'curranoi']

for user in superusers:
    print 'Adding '+user
    u = User(username=user)
    u.set_password(user)
    u.is_superuser = True
    u.is_staff = True
    u.save()
