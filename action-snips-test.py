#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import requests
import datetime
import untangle

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

latitude = '59.933333'
longitude = '10.716667'

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()
 

#def numbers_to_strings(argument):
#    switcher = {
#        0: "zero",
#        1: "one",
#        2: "two",
#    }
#    return switcher.get(argument, "nothing")


def precipitation_next_hours():
    r = requests.get('https://api.met.no/weatherapi/nowcast/0.9/?lat='+latitude+'&lon='+longitude)
    data = untangle.parse(r.content)
    
    millimeter = 0
    times = data.weatherdata.product.time

    return len(times)+' '+millimeter
    
    # for t in times:
    #    millimeter +=  float(t.location.precipitation['value'])
    
    # return 'in the next hours it will rain an average of '+str(millimeter / len(times))+' millimeters per hour'


# def extrem_data_norway():
#     r = requests.get('https://api.met.no/weatherapi/extremeswwc/1.2/')
#     data = untangle.parse(r.content)
    
#     precipitation_place = data.weatherdata.product.time[0].maximumPrecipitations.location[0]['name']
#     precipitation_value = data.weatherdata.product.time[0].maximumPrecipitations.location[0].maximumPrecipitation['value']
    
#     temperature_min_place = data.weatherdata.product.time[0].lowestTemperatures.location[0]['name']
#     temperature_min_value = data.weatherdata.product.time[0].lowestTemperatures.location[0].lowestTemperature['value']
    
#     temperature_max_place = data.weatherdata.product.time[0].highestTemperatures.location[0]['name']
#     temperature_max_value = data.weatherdata.product.time[0].lowestTemperatures.location[0].highestTemperature['value']
    
#     return 'in norway in the last 24 hours\
#     the most rain fell in '+precipitation_place+' with '+precipitation_value+' millimeters.\
#     the coldest place was '+temperature_min_place+' with '+temperature_min_value+' degree celsius.\
#     the warmest place was '+temperature_max_place+' with '+temperature_max_value+' degree celsius.'


# def moon_phase():
#     now = datetime.datetime.now()
    
#     r = requests.get('https://api.met.no/weatherapi/sunrise/1.1/?lat='+latitude+'&lon='+longitude+'&date='+now.strftime("%Y-%m-%d"))
#     data = untangle.parse(r.content)
    
#     return 'the moon phase today is '+data.astrodata.time.location.moon['phase']


# def sun_rise_set():
#     now = datetime.datetime.now()
    
#     r = requests.get('https://api.met.no/weatherapi/sunrise/1.1/?lat='+latitude+'&lon='+longitude+'&date='+now.strftime("%Y-%m-%d"))
#     data = untangle.parse(r.content)
    
#     sun_rise = data.astrodata.time.location.sun['rise']
#     sun_rise = datetime.datetime.strptime(sun_rise[:19], '%Y-%m-%dT%H:%M:%S')
    
#     sun_set = data.astrodata.time.location.sun['set']
#     sun_set = datetime.datetime.strptime(sun_set[:19], '%Y-%m-%dT%H:%M:%S')
    
#     return 'the sun rises at '+sun_rise.strftime("%H %M").replace('0', '')+' and sets at '+sun_set.strftime("%H %M").replace('0', '')


# def date_now():
#     date = now.strftime("%Y %m %d")
    
#     return date


# def latest_news_nrk():
#     r = requests.get('https://www.nrk.no/toppsaker.rss')
#     data = untangle.parse(r.content)

#     return 'here are the latest top news - '+\
#     data.rss.channel.item[0].title.cdata+' - '+data.rss.channel.item[0].description.cdata+' - '+\
#     data.rss.channel.item[1].title.cdata+' - '+data.rss.channel.item[1].description.cdata+' - '+\
#     data.rss.channel.item[2].title.cdata+' - '+data.rss.channel.item[2].description.cdata


# def wikipedia():
#     r = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/Felinae')
#     data = r.json()
    
#     return = data['extract']


def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, precipitation_next_hours())


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("gonzalez:Pets", subscribe_intent_callback) \
         .start()
