import datetime
from django.db.models import Q

from statsonice.models import Country

MONTHS = [datetime.date(2000,i,1).strftime('%B') for i in range(1,13)]

SKATER_FIELD_TYPES = {
    'skatername':           'Name',
    'country':              'Country',
    'dob':                  'Date',
    'dob_range':            'DateRange',
    'gender':               'Gender',
    'height':               'Number',
    'height_range':         'NumberRange',
    'start_year':           'Number',
    'start_year_range':     'NumberRange',
    'coach':                'Name',
    'choreographer':        'Name',
}
COMPETITION_FIELD_TYPES = {
    'name':                 'String',
    'country':              'Country',
    'start_date':           'Date',
    'start_date_range':     'DateRange',
    'isu_identifier':       'String',
}

class GeneralSearch:
    def __init__(self, objects):
        self.objects = objects

    # Given search params and field types, filter down self.objects
    #
    def general_search(self, search_params, field_types):

        # Combine multi field searches
        for field, field_type in field_types.items():
            if field_type == 'Date' or field_type == 'DateRange':
                search_params[field] = ['','','']
                if field+'_year' in search_params.keys():
                    search_params[field][0] = search_params[field+'_year']
                    del search_params[field+'_year']
                if field+'_month' in search_params.keys():
                    search_params[field][1] = search_params[field+'_month']
                    del search_params[field+'_month']
                if field+'_day' in search_params.keys():
                    search_params[field][2] = search_params[field+'_day']
                    del search_params[field+'_day']

        # Remove empty filters
        for key in search_params.keys():
            if search_params[key] == '':
                del search_params[key]
                continue
            if type(search_params[key]) == list:
                empty = True
                for x in search_params[key]:
                    if x != '':
                        empty = False
                        break
                if empty:
                    del search_params[key]
                    continue

        # Combine range data
        for key in search_params.keys():
            if key+'_range' in search_params.keys():
                search_params[key+'_range'] = [search_params[key], search_params[key+'_range']]
                del search_params[key]

        # Run the filters
        for field, value in search_params.items():
            try:
                field_type = field_types[field]
            except:
                return 'Field '+field+' not supported'
            if field_type == 'String':
                status = self.substring_filter(field, value)
            elif field_type == 'Gender':
                status = self.gender_filter(field, value)
            elif field_type == 'Date':
                status = self.date_filter(field, value)
            elif field_type == 'DateRange':
                status = self.date_range_filter(field, value)
            elif field_type == 'Number':
                status = self.number_filter(field, value)
            elif field_type == 'NumberRange':
                status = self.number_range_filter(field, value)
            elif field_type == 'Name':
                status = self.name_filter(field, value)
            elif field_type == 'Country':
                status = self.country_filter(field, value)
            else:
                return 'Field of type '+field_type+' not supported'
            if type(status) == str or type(status) == unicode:
                return status
        self.objects = self.objects.distinct()
        return self.objects

    # Filter self.objects based by matching the field with a value

    def gender_filter(self, field, value):
        if value == 'Female':
            value = 'F'
        elif value == 'Male':
            value = 'M'
        if value != 'M' and value != 'F':
            return value+' is not a valid gender'
        args = {field:value}
        self.objects = self.objects.filter(**args)

    def substring_filter(self, field, value):
        values = value.split(' ')
        for term in values:
            args = {field+'__icontains':term}
            self.objects = self.objects.filter(**args)

    def date_filter(self, field, value):
        if len(value) != 3:
            return "You have entered an invalid date"
        date = self.get_date(value, None)
        if type(date) == str:
            return date
        if date[0] != None:
            args = {field+'__year':date[0]}
            self.objects = self.objects.filter(**args)
        if date[1] != None:
            args = {field+'__month':date[1]}
            self.objects = self.objects.filter(**args)
        if date[2] != None:
            args = {field+'__day':date[2]}
            self.objects = self.objects.filter(**args)


    def date_range_filter(self, field, value):
        field = field[0:-6]
        start = value[0]
        end = value[1]
        if len(start) != 3 or len(end) != 3:
            return "You have entered an invalid date"
        start = self.get_date(start, False)
        end = self.get_date(end, True)
        if type(start) == str:
            return start
        if type(end) == str:
            return end
        if start[0] == 0 or end[0] == 9999:
            return 'You must include years in the range'
        args = {field+'__range':(datetime.date(*start), datetime.date(*end))}
        self.objects = self.objects.filter(**args)

    def get_date(self, value, last_day = None):
        try:
            value = [x.strip() for x in value]
            if value[1] == 'Month' or value[1] == '':
                value[1] = None
            else:
                value[1] = MONTHS.index(value[1])+1
            if value[0] == '':
                value[0] = None
            else:
                value[0] = int(value[0])
            if value[2] == '':
                value[2] = None
            else:
                value[2] = int(value[2])
            if last_day == None:
                return value
            if last_day:
                if value[0] == None:
                    value[0] = 9999
                if value[1] == None:
                    value[1] = 12
                if value[2] == None:
                    date = datetime.date(value[0], value[1], 1) - datetime.timedelta(1)
                    value[2] = date.day
                return value
            else:
                if value[0] == None:
                    value[0] = 0
                if value[1] == None:
                    value[1] = 1
                if value[2] == None:
                    value[2] = 1
                return value
        except:
            return str(value)+" is an invalid date"

    def number_filter(self, field, value):
        try:
            value = int(value)
        except:
            return str(value)+' is not a number'
        args = {field:int(value)}
        self.objects = self.objects.filter(**args)

    def number_range_filter(self, field, value):
        field = field[0:-6]
        try:
            value = [int(x) for x in value]
        except:
            return 'Some values in '+str(value)+' are not numbers'
        low = value[0]
        high = value[1]
        if low > high:
            low = value[1]
            high = value[0]
        args = {field+'__gte':low, field+'__lte':high}
        self.objects = self.objects.filter(**args)

    def name_filter(self, field, value):
        values = value.split(' ')
        for term in values:
            first_name = {field+'__first_name__icontains':term}
            last_name = {field+'__last_name__icontains':term}
            self.objects = self.objects.filter(Q(**first_name) | Q(**last_name))

    def country_filter(self, field, value):
        value = Country.get_country_code(value)
        if value == None:
            return 'You have entered an invalid country'
        args = {field+'__country_name':value}
        self.objects = self.objects.filter(**args)


