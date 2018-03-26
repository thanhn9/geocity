
import sys
#sys.path.insert(0,'../geocity')
#sys.path.insert(0,'/Users/thanguye/proj/geocity')

from flask import Flask
from flask import request
import re
import json
import bisect

app = Flask(__name__)

from geocity import data
from geocity import city


@app.route("/", strict_slashes=False)
def version():
    '''
    Main page, greeting..
    '''
    ver = '''
    <br><br>
    Geocity API version 0.0.1
    <br>
    &nbsp; &nbsp; by Thanh Nguyen
    <br>
    <br><br>
    &nbsp; &nbsp; <table>
    <tr><td> <a href="/2983268"> Sample return JSON format of a city info given geonameid</a> </td></tr>
    <tr><td> <a href="/2983268/longitude"> Get longitude value of a city info given geonameid</a> </td></tr>
    </table>
    '''
    return ver


@app.route('/proximity/<cityid>/<k>', methods=['GET'], strict_slashes=False)
@app.route('/proximity/<cityid>/<k>/<country_code>', methods=['GET'], strict_slashes=False)
def proximity(cityid, k, country_code=None):
    '''
    Query for the 'k' closest cities to cityid where closeness is measured by
    distance of its latitude and longitude.
    '''
    try:
        k = int(k)
    except ValueError as e:
        k = -1
    if k <= 0:
        return json.dumps(None)
    result = {}
    closest = []
    if cityid not in citydata.result:
        return json.dumps(None)

    cityobj = citydata.result[cityid]
    for cid in citydata.result:
        if cid == cityid:
            continue
        cityobj1 = citydata.result[cid]
        if country_code:
            if cityobj1.country_code.lower() != country_code.lower():
                continue
        distant = cityobj1 - cityobj
        if distant not in result:
            result[distant] = [cid]
            bisect.insort(closest, distant)
        else:
            result[distant].append(cid)
    closest_result = []
    i = 0
    for d in closest:
        for r in result[d]:
            info = citydata.result[r]
            closest_result.append({
                'geonameid': r, 
                'country_code': info.country_code, 
                'cityname': info.name, 
                'distance(miles)': d})
            i += 1
            if i >= k:
                return json.dumps(closest_result)
    return json.dumps(closest_result)

@app.route('/query/<regex>', methods=['GET'], strict_slashes=False)
def query(regex):
    result = []
    for gid in citydata.result:
        city = citydata.result[gid]
        match1 = re.findall(regex, city.alternatenames, re.I)
        match2 = re.findall(regex, city.asciiname, re.I)
        match3 = re.findall(regex, city.name, re.I)
        if match1 or match2 or match3:
            result.append(city_dict(city))
    return json.dumps(result)


@app.route('/distance/<cityid1>/<cityid2>', methods=['GET'], strict_slashes=False)
def distance(cityid1, cityid2):
    '''
    Return the distance between 2 cities in miles.
    '''
    if cityid1 not in citydata.result:
        return json.dumps(None)
    if cityid2 not in citydata.result:
        return json.dumps(None)
    cityobj1 = citydata.getcity(cityid1)
    cityobj2 = citydata.getcity(cityid2)
    return json.dumps(cityobj1 - cityobj2)

@app.route('/<geonameid>', methods=['GET'], strict_slashes=False)
@app.route('/<geonameid>/<attribute>', methods=['GET'], strict_slashes=False)
def attribute_value(geonameid, attribute=None):
    '''
    Return attribute value of a city given a geonameid and attribute name.
    If no attribute name is given, a specified city profile is returned 
    based on the geonameid.
    '''
    result = citydata.getcity(geonameid)
    if result:
        if attribute:
            return json.dumps(getattr(result, attribute))
    return json.dumps(city_dict(result))


def city_dict(cityobj):
    '''
    Turn City type object into a dict struture.
    '''
    if type(cityobj) != city.City:
        return None
    result = {}
    for attribute, _ in data.HEADER:
        value = getattr(cityobj, attribute)
        result[attribute] = value
    return result



if __name__ == "__main__":
    citydata = data.CityData()
    app.run()
