"""
This script assigns countries to cities
"""

import os
import sys
parent_path = os.path.dirname(os.path.realpath(__file__))+'/../util/'
sys.path.append(parent_path)
from get_settings import load_settings
load_settings(sys.argv)
import csv

from statsonice.models import City, Country

"""
geonameid         : integer id of record in geonames database
name              : name of geographical point (utf8) varchar(200)
asciiname         : name of geographical point in plain ascii characters, varchar(200)
alternatenames    : alternatenames, comma separated varchar(5000)
latitude          : latitude in decimal degrees (wgs84)
longitude         : longitude in decimal degrees (wgs84)
feature class     : see http://www.geonames.org/export/codes.html, char(1)
feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
country code      : ISO-3166 2-letter country code, 2 characters
cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
admin3 code       : code for third level administrative division, varchar(20)
admin4 code       : code for fourth level administrative division, varchar(20)
population        : bigint (8 byte int)
elevation         : in meters, integer
dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
timezone          : the timezone id (see file timeZone.txt) varchar(40)
modification date : date of last modification in yyyy-MM-dd format
"""

countries_file_location = 'data/countryInfo.txt'
cities_file_location = 'data/cities1000.txt'

# Read in countries file
handle = open(countries_file_location, 'rb')
reader = csv.reader(handle, delimiter="\t")
countries_data = {}
for row in reader:
    found = False
    for abbreviation, country in Country.COUNTRY_CHOICES:
        if row[4] == country:
            countries_data[row[0]] = abbreviation
            found = True
            break

# Read in cities file
handle = open(cities_file_location,'rb')
csv.field_size_limit(sys.maxsize)
reader = csv.reader(handle, delimiter="\t")
cities_data = {}
for row in reader:
    city = row[1]
    population = int(row[14])
    country_code_2 = row[8]
    if country_code_2 not in countries_data:
        continue
    country_code_3 = countries_data[country_code_2]
    if city in cities_data and cities_data[city][1] > population:
        continue
    cities_data[city] = [country_code_3, population]
    cities_data[city] = [country_code_3, population]
    for city in row[3].split(','):
        cities_data[city] = [country_code_3, population]
handle.close()


# Assign countries
for city in City.objects.all():
    if city.country == None:
        if city.city_name not in cities_data:
            continue
        country = Country.objects.get(country_name=cities_data[city.city_name][0])
        city.country = country
        skaters = city.home_city.all()
        if skaters.count() > 0:
            if skaters[0].country != city.country:
                city.country = skaters[0].country
        skaters = city.training_city.all()
        if skaters.count() > 0:
            if skaters[0].country != city.country:
                city.country = skaters[0].country
        print city.city_name+' in '+city.country.country_name

        #city.save()

# Hack based on some problems I've seen with the cities names
for city in City.objects.all():
    if city.country != None and city.city_name != None:
        continue
    city_name = city.city_name.split()
    if city_name == []:
        continue
    possible_country_code = city_name[-1].replace('(','').replace(')','')
    possible_country = Country.objects.filter(country_name=possible_country_code)
    if possible_country.count() == 1:
        city.country = possible_country[0]
        city.city_name = ' '.join(city_name[0:-1])
        try:
            print city.city_name
        except:
            print 'asdf'
        #city.save()
