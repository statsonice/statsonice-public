"""
These functions handle logging events on the website
"""

from django.core.mail import mail_admins

def log_event(subject, message):
    mail_admins(subject, message)
