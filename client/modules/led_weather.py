#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import re
import datetime
import struct
import urllib
import feedparser
import requests
import bs4
from client.app_utils import getTimezone
from semantic.dates import DateService

def replaceAcronyms(text):
    """
    Replaces some commonly-used acronyms for an improved verbal weather report.
    """

    def parseDirections(text):
        words = {
            'N': '북쪽',
            'S': '남쪽',
            'E': '동쪽',
            'W': '서쪽',
        }
        output = [words[w] for w in list(text)]
        return ' '.join(output)
    acronyms = re.findall(r'\b([NESW]+)\b', text)

    for w in acronyms:
        text = text.replace(w, parseDirections(w))

    text = re.sub(r'(\b\d+)F(\b)', '\g<1> Fahrenheit\g<2>', text)
    text = re.sub(r'(\b)mph(\b)', '\g<1>miles per hour\g<2>', text)
    text = re.sub(r'(\b)in\.', '\g<1>inches', text)

    return text


def get_locations():
    r = requests.get('http://www.wunderground.com/about/faq/' +
                     'international_cities.asp')
    
    # wonju KO  RKNW      37.33  127.95   150 47114

    soup = bs4.BeautifulSoup(r.text)
    data = soup.find(id="inner-content").find('pre').string
    # Data Stucture:
    #  00 25 location
    #  01  1
    #  02  2 region
    #  03  1
    #  04  2 country
    #  05  2
    #  06  4 ID
    #  07  5
    #  08  7 latitude
    #  09  1
    #  10  7 logitude
    #  11  1
    #  12  5 elevation
    #  13  5 wmo_id
    s = struct.Struct("25s1s2s1s2s2s4s5s7s1s7s1s5s5s")
    for line in data.splitlines()[3:]:
        row = s.unpack_from(line)
        info = {'name': row[0].strip(),
                'region': row[2].strip(),
                'country': row[4].strip(),
                'latitude': float(row[8].strip()),
                'logitude': float(row[10].strip()),
                'elevation': int(row[12].strip()),
                'id': row[6].strip(),
                'wmo_id': row[13].strip()}
        yield info


def get_forecast_by_name(location_name):
    entries = feedparser.parse("http://rss.wunderground.com/auto/rss_full/%s"
                               % urllib.quote(location_name))['entries']
    if entries:
        # We found weather data the easy way
        return entries
    else:
        # We try to get weather data via the list of stations
        for location in get_locations():
            if location['name'] == location_name:
                return get_forecast_by_wmo_id(location['wmo_id'])


def get_forecast_by_wmo_id(wmo_id):
    return feedparser.parse("http://rss.wunderground.com/auto/" +
                            "rss_full/global/stations/%s.xml"
                            % wmo_id)['entries']


def handle(text, profile):

    forecast = None
    if 'wmo_id' in profile:
        forecast = get_forecast_by_wmo_id(str(profile['wmo_id']))
    elif 'location' in profile:
        forecast = get_forecast_by_name(str(profile['location']))

    if not forecast:
        return

    tz = getTimezone(profile)

    service = DateService(tz=tz)
    date = service.extractDay(text)
    date = datetime.datetime.now(tz=tz)

    for entry in forecast:
        try:
            date_desc = entry['title'].split()[0].strip().lower()
            print(entry['title'], date_desc)
            if date_desc == 'forecast':
                # For global forecasts
                weather_desc = entry['description'].split(".")[0].strip().lower()
                if 'cloud' in weather_desc:
                    show_weather(cloud=(255, 255, 255))
                elif 'rain' in weather_desc:
                    show_weather(rain=(0, 0, 255))
                elif 'snow' in weather_desc:
                    show_weather(snow=(255, 255, 255))
                else:
                    show_weather(sun=(255, 0, 0))


            elif date_desc == 'current':
                # For first item of global forecasts
                continue
        except:
            continue
