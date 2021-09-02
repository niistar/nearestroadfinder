import requests
import json
import urllib.parse
from key import key_str as key
import math

def findNewLat(lat):
    return str(lat + (150 / 6371000) * (180 / math.pi))

def findNewLng(lat, lng):
    return str(lng + (150 / 6371000) * (180 / math.pi) / math.cos(lat * math.pi/180))

def generateParamsInput(input):
    return {'input': input, 'inputtype':'textquery', 'fields':'formatted_address,name,geometry', 'key': key}

def generateParamsCoords(lat, lng):
    coords = lat + ',' + lng

    params = {'points': coords, 'key': key}
    return urllib.parse.urlencode(params, safe=',')

def generateStreetView(lat, lng):
    return 'https://www.google.com/maps/embed/v1/streetview?key=' + key + '&location=' + lat + ',' + lng


def findplace(input):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'

    params = generateParamsInput(input)
    response = requests.get(url,params=params)

    coord = json.loads(response.text)
    lat = coord['candidates'][0]['geometry']['location']['lat']
    lng = coord['candidates'][0]['geometry']['location']['lng']
    snaproads(str(lat), str(lng))


def snaproads(lat, lng):
    url = 'https://roads.googleapis.com/v1/nearestRoads'
    
    pld = generateParamsCoords(lat, lng)
    response = requests.get(url,params=pld)

    jresp = response.json()

    if not jresp:
        new_lat = findNewLat(float(lat))
        new_lgt = findNewLng(float(lat), float(lng))
        snaproads(new_lat, new_lgt)
    else:
        print(jresp)
        lat_st = jresp['snappedPoints'][0]['location']['latitude']
        lng_st = jresp['snappedPoints'][0]['location']['longitude']
        print(generateStreetView(str(lat_st), str(lng_st)))

input = input('Digita ai o pourra: ')
findplace(input)