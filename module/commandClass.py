# -*- coding: cp949 -*-

import time
import random
import math
import urllib
import json
import parserClass

hour = time.localtime().tm_hour
parser = parserClass._parser()

class _command:
    

    def make_random_string(self):
        string = u""
        for i in range( random.randrange(6,9) ):
            string += str(random.randrange(0,10))
        return string
        
    def parsing(self,city):
        url = u"https://maps.googleapis.com/maps/api/geocode/json?address="
        other = u"&key=AIzaSyA1nJ8BFF1GNwAQi-vPzmxah77Ps1StyAI"
        
        parsed_data =  urllib.urlopen((url+city+other).encode('utf8')).read()
        r_data = json.loads(parsed_data)
        
        if r_data['status'] == u'OK':
            data = r_data['results'][0]
            lat = round( float(data['geometry']['location']['lat']), 1)
            lng = round( float(data['geometry']['location']['lng']), 1)
            address = data['formatted_address']

            s = address.split(',')
            if(len(s)>3):
                address = (s[0]+", "+s[1]+", "+s[2])

            return { 'address':address, 'lat':lat, 'lng':lng }
        else:
            return { }


    def make_str(self,text):
        string = u""
        data = self.parsing(text)
        
        if len(data) == 0:
            return u"해당 주소를 찾지 못했습니다. 조금 더 일반적인 주소를 불러주세요."

        string += data['address']+'\n'
        string += parser.make_city_desc_geo(data['lat'],data['lng'])

        return string
            
            


    def handle(self, text, id, name):
        #type(text) == str
        string = u"@{0}\n{1} ".format( name, self.make_str(text) )
        return string



    def test(self, text):
        print self.handle(text,'33333','test')
