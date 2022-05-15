import urllib.request
import requests
import threading
import time

class ThingSpeak:
    
    def enviar(self, lat, lon, val1, val2):
        URL='https://api.thingspeak.com/update?api_key='
        KEY='8HRAZHU8AWKCO3HN'
        HEADER='&field1={}&field2={}&field3={}&field4={}'.format(lat, lon, val1, val2)
        NEW_URL=URL+KEY+HEADER
        urllib.request.urlopen(NEW_URL)
        
##CANAL: https://thingspeak.com/channels/1727290