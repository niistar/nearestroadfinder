import requests
import json
import urllib.parse
from key import key_str as key

def findplace(input):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = {'input': input, 'inputtype':'textquery', 'fields':'formatted_address,name,geometry', 'key': key}

    response = requests.get(url,params=params)

    coord = json.loads(response.text)
    lat = coord['candidates'][0]['geometry']['location']['lat']
    lng = coord['candidates'][0]['geometry']['location']['lng']
    snaproads(str(lat), str(lng))


def snaproads(lat, lng):
    url = 'https://roads.googleapis.com/v1/nearestRoads'
    coords = lat + ',' + lng

    params = {'points': coords, 'key': key}
    pld = urllib.parse.urlencode(params, safe=',')

    response = requests.get(url,params=pld)
    print(response.url)
    print(json.loads(response.text))

input = input('Digita ai o pourra: ')
findplace(input)