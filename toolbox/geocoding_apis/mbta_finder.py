"""
author: Kevin Crispie

Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def encode_maps_url(place_name):
    base_url = "https://maps.googleapis.com/maps/api/geocode/"
    place_name = place_name.replace(' ','%20')
    url = base_url + place_name

    return url


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """

    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)

    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """

    url = encode_maps_url(place_name)
    print url
    result = get_json(url)
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']
    
    return lat, lng


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    base_url = "http://realtime.mbta.com/developer/api/v2/stopsbylocation?" + \
    "api_key=wX9NwuHnZU2ToO7GmGR9uw&lat=latitude&lon=longitude&format=json"

    url_with_lng = base_url.replace('latitude',latitude)
    url_with_lat_lng = url_with_lng.replace('longitude', longitude)

    results = get_json(url_with_lat_lng)
    
    return results
    


def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the 
    distance from the given place to that stop.
    """



    pass

print get_lat_long("Fenway Park")