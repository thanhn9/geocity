
import re
import codecs
import city

__doc__ = '''
The main 'geoname' table has the following fields :
    ---------------------------------------------------
    geonameid         : integer id of record in geonames database
    name              : name of geographical point (utf8) varchar(200)
    asciiname         : name of geographical point in plain ascii characters, varchar(200)
    alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
    latitude          : latitude in decimal degrees (wgs84)
    longitude         : longitude in decimal degrees (wgs84)
    feature class     : see http://www.geonames.org/export/codes.html, char(1)
    feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
    country code      : ISO-3166 2-letter country code, 2 characters
    cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
    admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
    admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
    admin3 code       : code for third level administrative division, varchar(20)
    admin4 code       : code for fourth level administrative division, varchar(20)
    population        : bigint (8 byte int) 
    elevation         : in meters, integer
    dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
    timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
    modification date : date of last modification in yyyy-MM-dd format

'''

# may be used for type validation
HEADER = [
    ['geonameid', int],
    ['name', str], 
    ['asciiname', str], 
    ['alternatenames', str],
    ['latitude', float],  
    ['longitude', float], 
    ['feature_class', str],
    ['feature_code', str],
    ['country_code', str],
    ['cc2', str], 
    ['admin1_code', str], 
    ['admin2_code', str], 
    ['admin3_code', str], 
    ['admin4_code', str],
    ['population', int],
    ['elevation', int],
    ['dem', int], 
    ['timezone', str], 
    ['modification_date', str] 
]

# not used now
Feature_classes = {
    'A': 'country, state, region,...',
    'H': 'stream, lake, ...',
    'L': 'parks,area, ...',
    'P': 'city, village,...',
    'R': 'road, railroad ',
    'S': 'spot, building, farm',
    'T': 'mountain,hill,rock,... ',
    'U': 'undersea',
    'V': 'forest,heath,...'
}

# not used now
Continent_codes = {
    'AF' : {'name': 'Africa', 'geonameId': 6255146},
    'AS' : {'name': 'Asia', 'geonameId': 6255147},
    'EU' : {'name': 'Europe', 'geonameId': 6255148},
    'NA' : {'name': 'North America', 'geonameId': 6255149},
    'OC' : {'name': 'Oceania', 'geonameId': 6255151},
    'SA' : {'name': 'South America', 'geonameId': 6255150},
    'AN' : {'name': 'Antarctica', 'geonameId': 6255152}
}


# not used now, might need it for type validation
class Alternatename(object):
    def __init__(self):
        self.alternateNameId = 0
        self.geonameid = 0
        self.isolanguage = None
        self.alternate_name = None
        self.isPreferredName = False
        self.isShortName = False
        self.isColloquial = False
        self.isHistoric = False

    def _validate(self):
        if not self.alternateNameId == int:
            raise TypeError('alternateNameId should be an int type')
        if not type(self.geonameid) == int:
            raise TypeError('geonameid should be an int type')
        if not (type(self.isolanguage) == str and len(self.isolanguage) > 7):
            raise TypeError('isolange should be str , var(7)')
        if not (type(self.alternate_name) == str and len(self.alternate_name) > 400):
            raise TypeError('alternate_name should be str , var(400)')
        if not type(self.isPreferredName) == bool:
            raise TypeError('isPreferredName should be a bool type')
        if not type(self.isShortName) == bool:
            raise TypeError('isShortName should be a bool type')
        if not type(self.isColloquial) == bool:
            raise TypeError('isColloquial should be a bool type')
        if not type(self.isHistoric) == bool:
            raise TypeError('isHistoric should be a bool type')


class CityData(object):
    '''
    Representation of city data.
    '''
    def __init__(self, datafile='data/cities1000.txt', header=HEADER, separator='\t'):
        self.datafile = datafile
        self.separator = separator
        self.data = None
        self.result = {}
        with codecs.open(self.datafile, 'r', 'utf-8') as f:
            self.data = f.readlines()
        self._parse()

    def _checkdata_item_count(self):
        pass

    def _checkdata_types(self):
        pass

    def _parse(self):
        '''
        Parse the given data, and store it to result.
        '''
        header_length = len(HEADER)
        for i in range(len(self.data)):
            line = self.data[i].rstrip('\r\n')
            if re.findall(r'^\s*$', line):
                continue
            data_items = line.split(self.separator)

            #
            # self._checkdata_item_count()
            #
            if len(data_items) != header_length:
                print "data item line number:", i,  data_items
                print len(data_items), '=?', header_length
                raise ValueError('Data item count mismatched')

            #
            # self._checkdata_types()
            #
            # data_items[0] ---> int

            res = {}
            for ii, value in enumerate(data_items):
                res[HEADER[ii][0]] = value
            self.result[data_items[0]] = city.City(res)

    def _display(self, geonameid):
        '''
        Display the entry for a given geonameid.
        '''
        if geonameid in self.result:
            c = self.result[geonameid]
            c.display()
            #for key, value in r.items():
            #    print '  ', key,":",  value.encode('utf-8')
        else:
            print '*geonameid key', geonameid, 'does not exist'

    def _displayall(self):
        for k in self.result.keys():
            self._display(geonameid=k)

    def getcity(self, geonameid):
        '''
        Get a city entry profile by geonameid.
        '''
        return self.result.get(geonameid)



if __name__ == '__main__':
    citydata = CityData()
    #citydata._displayall()
    citydata._display(geonameid='2983268')
