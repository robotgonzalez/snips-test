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

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    #r = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/Felinae')
    #data = r.json()
    #result_sentence = data['extract']
    
    now = datetime.datetime.now()
    date = now.strftime("%Y %m %d")
    #time = now.strftime("%H %M")
    
    result_sentence = date
    
    #print(date)
    
    r = requests.get('https://api.met.no/weatherapi/sunrise/1.1/?lat=62.308611&lon=6.937222&date='+now.strftime("%Y-%m-%d"))
    doc = untangle.parse(r.content)

    sun_rise = doc.astrodata.time.location.sun['rise']
    sun_rise = datetime.datetime.strptime(sun_rise[:19], '%Y-%m-%dT%H:%M:%S')
    
    sun_set = doc.astrodata.time.location.sun['set']
    sun_set = datetime.datetime.strptime(sun_set[:19], '%Y-%m-%dT%H:%M:%S')
    
    result_sentence = 'the sun rises at '+sun_rise.strftime("%H %M").replace('0', '')+' and sets at '+sun_set.strftime("%H %M").replace('0', '')
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("gonzalez:Pets", subscribe_intent_callback) \
         .start()
