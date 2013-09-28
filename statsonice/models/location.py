# country class
from django.db import models
from statsonice.models.models_validator import LocationValidator

class Country(models.Model):
    COUNTRY_CHOICES = (
        ('', ''),
        ('AFG', 'Afghanistan'),
        ('ALB', 'Albania'),
        ('ALG', 'Algeria'),
        ('AND', 'Andorra'),
        ('ANG', 'Angola'),
        ('ANT', 'Antigua and Barbuda'),
        ('ARG', 'Argentina'),
        ('ARM', 'Armenia'),
        ('ARU', 'Arbua'),
        ('ASA', 'American Samoa'),
        ('AUS', 'Australia'),
        ('AUT', 'Austria'),
        ('AZE', 'Azerbaijan'),
        ('BAH', 'Bahamas'),
        ('BAN', 'Bangladesh'),
        ('BAR', 'Barbados'),
        ('BDI', 'Burundi'),
        ('BEL', 'Belgium'),
        ('BEN', 'Benin'),
        ('BER', 'Bermuda'),
        ('BHU', 'Bhutan'),
        ('BIH', 'Bosnia and Herzegovina'),
        ('BIZ', 'Belize'),
        ('BLR', 'Belarus'),
        ('BOL', 'Bolivia'),
        ('BOT', 'Botswana'),
        ('BRA', 'Brazil'),
        ('BRN', 'Bahrain'),
        ('BRU', 'Brunei'),
        ('BUL', 'Bulgaria'),
        ('BUR', 'Burkina Faso'),
        ('CAF', 'Central African Republic'),
        ('CAM', 'Cambodia'),
        ('CAN', 'Canada'),
        ('CAY', 'Cayman Islands'),
        ('CGO', 'Congo'),
        ('CHA', 'Chad'),
        ('CHI', 'Chile'),
        ('CHN', 'China'),
        ('CIV', 'Cote d\'Ivoire'),
        ('CMR', 'Cameroon'),
        ('COD', 'Democratic Republic of the Congo'),
        ('COK', 'Cook Islands'),
        ('COL', 'Colombia'),
        ('COM', 'Comoros'),
        ('CPV', 'Cape Verde'),
        ('CRC', 'Costa Rica'),
        ('CRO', 'Croatia'),
        ('CUB', 'Cuba'),
        ('CYP', 'Cyprus'),
        ('CZE', 'Czech Republic'),
        ('DEN', 'Denmark'),
        ('DJI', 'Djibouti'),
        ('DMA', 'Dominica'),
        ('DOM', 'Dominican Republic'),
        ('ECU', 'Ecuador'),
        ('EGY', 'Egypt'),
        ('ERI', 'Eritrea'),
        ('ESA', 'El Salvador'),
        ('ESP', 'Spain'),
        ('EST', 'Estonia'),
        ('ETH', 'Ethiopia'),
        ('FIJ', 'Fiji'),
        ('FIN', 'Finland'),
        ('FRA', 'France'),
        ('FSM', 'Micronesia'),
        ('GAB', 'Gabon'),
        ('GAM', 'Gambia'),
        ('GBR', 'Great Britain'),
        ('GBS', 'Guinea-Bissau'),
        ('GEO', 'Georgia'),
        ('GEQ', 'Equitorial Guinea'),
        ('GER', 'Germany'),
        ('GHA', 'Ghana'),
        ('GRE', 'Greece'),
        ('GRN', 'Grenada'),
        ('GUA', 'Guatemala'),
        ('GUI', 'Guinea'),
        ('GUM', 'Guam'),
        ('GUY', 'Guyana'),
        ('HAI', 'Haiti'),
        ('HKG', 'Hong Kong'),
        ('HON', 'Honduras'),
        ('HUN', 'Hungary'),
        ('INA', 'Indonesia'),
        ('IND', 'India'),
        ('IRI', 'Iran'),
        ('IRL', 'Ireland'),
        ('IRQ', 'Iraq'),
        ('ISL', 'Iceland'),
        ('ISR', 'Israel'),
        ('ISV', 'Virgin Islands'),
        ('ITA', 'Italy'),
        ('IVB', 'British Virgin Islands'),
        ('JAM', 'Jamaica'),
        ('JOR', 'Jordan'),
        ('JPN', 'Japan'),
        ('KAZ', 'Kazakhstan'),
        ('KEN', 'Kenya'),
        ('KGZ', 'Kyrgyzstan'),
        ('KIR', 'Kiribati'),
        ('KOR', 'South Korea'),
        ('KSA', 'Saudi Arabaia'),
        ('KUW', 'Kuwait'),
        ('LAO', 'Laos'),
        ('LAT', 'Latvia'),
        ('LBA', 'Libya'),
        ('LBR', 'Liberia'),
        ('LCA', 'Saint Lucia'),
        ('LES', 'Lesotho'),
        ('LIB', 'Lebanon'),
        ('LIE', 'Liechtenstein'),
        ('LTU', 'Lithuania'),
        ('LUX', 'Luxembourg'),
        ('MAD', 'Madagascar'),
        ('MAR', 'Morocco'),
        ('MAS', 'Malaysia'),
        ('MAW', 'Malawi'),
        ('MDA', 'Moldova'),
        ('MDV', 'Maldives'),
        ('MEX', 'Mexico'),
        ('MGL', 'Mongolia'),
        ('MHL', 'Marshall Islands'),
        ('MKD', 'Macedonia'),
        ('MLI', 'Meli'),
        ('MLT', 'Malta'),
        ('MNE', 'Montenegro'),
        ('MON', 'Monaco'),
        ('MOZ', 'Mozambique'),
        ('MRI', 'Mauritius'),
        ('MTN', 'Mauritania'),
        ('MYA', 'Myanmar'),
        ('NAM', 'Namibia'),
        ('NCA', 'Nicaragua'),
        ('NED', 'Netherlands'),
        ('NEP', 'Nepal'),
        ('NGR', 'Nigeria'),
        ('NIG', 'Niger'),
        ('NOR', 'Norway'),
        ('NRU', 'Nauru'),
        ('NZL', 'New Zealand'),
        ('OMA', 'Oman'),
        ('PAK', 'Pakistan'),
        ('PAN', 'Panama'),
        ('PAR', 'Paraguay'),
        ('PER', 'Peru'),
        ('PHI', 'Philippines'),
        ('PLE', 'Palestine'),
        ('PLW', 'Palau'),
        ('PNG', 'Papua New Guinea'),
        ('POL', 'Poland'),
        ('POR', 'Portugal'),
        ('PRK', 'North Korea'),
        ('PUR', 'Puerto Rico'),
        ('QAT', 'Qatar'),
        ('ROM', 'Romania'),
        ('ROU', 'Romania'),
        ('RSA', 'South Africa'),
        ('RUS', 'Russia'),
        ('RWA', 'Rwanda'),
        ('SAM', 'Samoa'),
        ('SEN', 'Senegal'),
        ('SER', 'Serbia'),
        ('SEY', 'Seychelles'),
        ('SIN', 'Singapore'),
        ('SKN', 'Saint Kitts and Nevis'),
        ('SLE', 'Sierra Leone'),
        ('SLO', 'Slovenia'),
        ('SMR', 'San Marino'),
        ('SOL', 'Solomon Islands'),
        ('SOM', 'Somalia'),
        ('SRB', 'Serbia'),
        ('SRI', 'Sri Lanka'),
        ('STP', 'Sao Tome and Principe'),
        ('SUD', 'Sudan'),
        ('SUI', 'Switzerland'),
        ('SUR', 'Suriname'),
        ('SVK', 'Slovakia'),
        ('SWE', 'Sweden'),
        ('SWZ', 'Swaziland'),
        ('SYR', 'Syria'),
        ('TAN', 'Tanzania'),
        ('TGA', 'Tonga'),
        ('THA', 'Thailand'),
        ('TJK', 'Tajikistan'),
        ('TKM', 'Turkmenistan'),
        ('TLS', 'Timor-Leste'),
        ('TOG', 'Togo'),
        ('TPE', 'Chinese Taipei'),
        ('TRI', 'Trinidad and Tobago'),
        ('TUN', 'Tunisia'),
        ('TUR', 'Turkey'),
        ('TUV', 'Tuvalu'),
        ('UAE', 'United Arab Emirates'),
        ('UGA', 'Uganda'),
        ('UKR', 'Ukraine'),
        ('URU', 'Uruguay'),
        ('USA', 'United States of America'),
        ('UZB', 'Uzbekistan'),
        ('VAN', 'Vanuatu'),
        ('VEN', 'Venezuela'),
        ('VIE', 'Vietnam'),
        ('VIN', 'Saint Vincent and the Grenadines'),
        ('YEM', 'Yemen'),
        ('ZAM', 'Zambia'),
        ('ZIM', 'Zimbabwe'),

        # NON-ISO Country Codes
        ('AHO', 'Netherlands Antilles'),
        ('ANZ', 'Australasia'),
        ('BOH', 'Bohemia'),
        ('BWI', 'British West Indies'),
        ('EUA', 'Unified Team of Germany'),
        ('EUN', 'Unified Team'),
        ('FRG', 'West Germany'),
        ('GDR', 'East Germany'),
        ('RU1', 'Russian Empire'),
        ('SCG', 'Serbia and Montenegro'),
        ('TCH', 'Czechoslovakia'),
        ('URS', 'Soviet Union'),
        ('YUG', 'Yugoslavia'),
        ('ZZX', 'Mixed teams'),
        ('BIR', 'Burma'),
        ('CEY', 'Ceylon'),
        ('DAH', 'Dahomey'),
        ('HBR', 'British Honduras'),
        ('KHM', 'Khmer Republic'),
        ('MAL', 'Malaya'),
        ('NBO', 'North Borneo'),
        ('NRH', 'Northern Rhodesia'),
        ('RAU', 'United Arab Republic'),
        ('RHO', 'Rhodesia'),
        ('ROC', 'Republic of China'),
        ('SAA', 'Saar'),
        ('UAR', 'United Arab Republic'),
        ('VOL', 'Upper Volta'),
        ('YAR', 'North Yemen'),
        ('YMD', 'South Yemen'),
        ('ZAI', 'Zaire'),
    )
    country_name = models.CharField(max_length = 4,
                                    choices = COUNTRY_CHOICES,
                                    default = '',
                                    primary_key=True,
                                    blank=True,)

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Country %s)' % (self.country_name)
    def clean(self):
        LocationValidator.validate_country(self)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Country, self).save(*args, **kwargs)

    # Get the English country name
    #
    def get_country_name(self):
        for code, name in self.COUNTRY_CHOICES:
            if code == self.country_name:
                return name
        return None

    @staticmethod
    def get_country_code(country_name):
        for code, name in Country.COUNTRY_CHOICES:
            if country_name == name:
                return code
        return None





class City(models.Model):
    city_name = models.CharField(max_length = 100)
    country = models.ForeignKey(Country, null=True)

    class Meta:
        app_label = 'statsonice'

    def __unicode__(self):
        return u'(City %s)' % (self.city_name)
