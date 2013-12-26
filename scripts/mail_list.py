"""
Mass mail everyone subscribed to mailing list given a file
"""

import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)

from django.core import mail

from statsonice.models import User


# Find all emails that are on mailing list
users = User.objects.filter(userinfo__mailing_list = True)
recipient_list = users.values_list('email', flat=True)
print "Sending to",recipient_list

# Read data for email
# TODO: Move this to a database table
from_email = "admin@statsonice.com"
subject = "test subject"
body = "test body"

# Send mass mail
messages = [(subject, body, from_email, recipient_list)]

mail.send_mass_mail(messages)
