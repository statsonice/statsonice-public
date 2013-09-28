from django.db import models

# Model to store lots of random settings data as key/value pairs
#
class Settings(models.Model):
    key = models.CharField(max_length = 16, primary_key=True)
    value = models.CharField(max_length = 500)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Other %s)' % (self.key)
    @staticmethod
    def get_value(key):
        return Settings.objects.get(key=key).value
