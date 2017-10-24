
from geopy.distance import vincenty
import data

class City(object):
    '''
    Representation of a city data structure.
    '''
    def __init__(self, datadict):
        self.datadict = datadict
        for i,_ in data.HEADER:
            setattr(self, i, self.datadict[i])

    def display(self):
        print "******Cityid:", self.geonameid, "****"
        for attribute, _ in data.HEADER:
            value = getattr(self, attribute)
            print '    ', attribute, ':', value 

    def __sub__(self, cityobj):
        '''
        Overload minus sign used as a distance method name.  Here the distance 
        function 'vincenty' is used to calculate the distance between pairs of 
        geo (longitude, latitude)
        '''
        if type(cityobj) == City:
            c1 = (float(self.latitude), float(self.longitude))
            c2 = (float(cityobj.latitude), float(cityobj.longitude))
            #from geopy.distance import great_circle
            #return great_circle(c1, c2)
            return vincenty(c1, c2).miles


if __name__ == '__main__':
    citydata = data.CityData()
    citylist = []

    for idd, cityobj in citydata.result.items():
        citylist.append(cityobj)
    c1 = citylist[0]
    c1.display()

    c2 = citylist[1]
    c2.display()

    # computing distance
    d1 = c1-c2
    d2 = c2-c1
    print 'distance c1-c2', d1
    print 'distance c2-c1', d2
    d3 = c1-c1
    print 'distance c1-c1', d3

    print d1 > d3, "should be true"
    print d1 == d2, "should be true"
