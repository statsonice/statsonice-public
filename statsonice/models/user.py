from datetime import date

from django.db import models
from django.contrib.auth.models import User

from statsonice.models.location import Country

# User model (for reference)
# class User(models.Model):
#     username
#     password
#     email
#     first_name
#     last_name


# This is basically an extension of the User model
class UserInfo(models.Model):
    user = models.OneToOneField(User)
    register_date = models.DateField(auto_now_add=True)
    last_login = models.DateField()
    country = models.ForeignKey(Country, null=True, blank=True)
    mailing_list = models.BooleanField(default=False)

    def is_subscribed(self):
        for subscription in self.subscription_set.all():
            if subscription_start <= date.today() and subscription_end >= date.today():
                return True
        return False
    class Meta:
        app_label = 'auth'
    def __unicode__(self):
        return u'(UserInfo for %s)' % (self.user.username)

class Subscription(models.Model):
    user_info = models.ForeignKey(UserInfo)
    subscription_start = models.DateField(null=True, blank=True)
    subscription_end = models.DateField(null=True, blank=True)
    class Meta:
        app_label = 'auth'
    def __unicode__(self):
        return u'(Subscription for %s)' % (self.user_info.user.username)
