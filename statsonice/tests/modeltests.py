from django.test import TestCase
from statsonice.models import *

class SkaterTestCase(TestCase):
    def setUp(self):
        """
        skater1 = Skater()
        skater1.country = Country.objects.get(country_name='USA')
        skater1.dob = datetime.strptime('January 2, 1993', '%B %d, %Y')
        skater1.gender = 'M'
        skater1.height = 100
        skater1.home_city = City.objects.get(city_name='Boston', country=Country.objects.get(country_name='USA'))
        skater1.training_city = City.objects.get(city_name='Moscow', country=Country.objects.get(country_name='RUS'))
        skater1.start_year = 2010
        skater1.save()
        skater1.coach = [Coach.objects.get(first_name='Mama', last_name='Bear')]
        skater1.choreographer = [Coach.objects.get(first_name='Papa', last_name='Bear')]
        skater1.save()
        """
    def test_view_name(self):
        return
    def test_url_name(self):
        return
    def test_url(self):
        return

