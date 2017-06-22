#-*- coding:utf-8 -*-
import urllib
import json
import aqiLog


class _parser():

    def __init__(self):
        self.url = "http://api.waqi.info/feed/"
        self.token = "/?token=9ff3406a39f472306334a01b262537d8e9fc9825"
        self.name = {'seoul':u'서울', 'incheon':u'인천', 'busan':u'부산', 'daegu':u'대구','daejeon':u'대전','gwangju':u'광주'}
        self.log = aqiLog._log()

    def get_data(self,city):
        self.log.update(u"parsing "+city+u" data")
        parsed_data = urllib.urlopen( self.url + city + self.token ).read()
        r_data = json.loads(parsed_data)

        data = r_data['data']

        PM10 = "null"
        PM25 = "null"


        if( data['iaqi'].has_key('pm10')):
            PM10 = data['iaqi']['pm10']['v']
        if( data['iaqi'].has_key('pm25')):
            PM25 = data['iaqi']['pm25']['v']
        AQI = data['aqi']

        return { "AQI":AQI, "PM10":PM10, "PM25":PM25 }

    def get_data_geo(self,lat,lng):
        self.log.update(u"parsing geo data")
        parsed_data = urllib.urlopen( self.url + "geo:"+str(lat)+";"+str(lng) + self.token ).read()
        r_data = json.loads(parsed_data)

        data = r_data['data']

        PM10 = "null"
        PM25 = "null"


        if( data['iaqi'].has_key('pm10')):
            PM10 = data['iaqi']['pm10']['v']
        if( data['iaqi'].has_key('pm25')):
            PM25 = data['iaqi']['pm25']['v']
        AQI = data['aqi']
        TIME = data['time']['s']

        return { "AQI":AQI, "PM10":PM10, "PM25":PM25, "TIME":TIME }
    

    def AQI_level_str(self,AQI):
        s = ""
        if AQI == "null":
            return u"자료 없음"
        
        if(AQI<=50):
            s = u"좋음"
        elif(AQI<=100):
            s = u"보통"
        elif(AQI<=150):
            s = u"나쁨"
        elif(AQI<=200):
            s = u"심각"
        elif(AQI<=300):
            s = u"매우 심각"
        elif(AQI>300):
            s = u"매우 위험"
        else:
            s = u""
        return s
            
    def super_fine_duse_str(self,dust):
        s = ""
        if(dust=="null"):
            return ""
        
        if(dust<=15):
            s = u"좋음"
        elif(dust<=40):
            s = u"보통"
        elif(dust<=100):
            s = u"나쁨"
        elif(dust>100):
            s = u"심각"
        else:
            s = u""
        return s

    def fine_duse_str(self,dust):
        s = ""
        if(dust=="null"):
            return ""
        
        if(dust<=30):
            s = u"좋음"
        elif(dust<=67):
            s = u"보통"
        elif(dust<=125):
            s = u"나쁨"
        elif(dust>125):
            s = u"심각"
        else:
            s = u""
        return s



    def make_city_desc(self,city):
        
        try:
            string = ""
            
            l = self.get_data(city)
            if self.name.has_key(city):
                string += ( u"" + self.name[city] + u" " )
            else:
                string += ( u"" + city + u" " )
            string += ( u"AQI:" + str(l['AQI']) + u"("+self.AQI_level_str(l['AQI'])+u")\n" )
            string += ( u"PM10:" + str(l['PM10']) + u"("+self.AQI_level_str(l['PM10'])+u") " )
            string += ( u"PM25:" + str(l['PM25']) + u"("+self.AQI_level_str(l['PM25'])+u")\n" )

            return string
        except BaseException as e:
            self.log.update(u"error occur in make_city_desc." + e.message)



    def make_city_desc_geo(self,lat,lng):
        
        try:
            string = ""
            l = self.get_data_geo(lat,lng)
            string += ( u"" + l['TIME'] + "\n" )
            string += ( u"AQI:" + str(l['AQI']) + u"("+self.AQI_level_str(l['AQI'])+u")\n" )
            string += ( u"PM10:" + str(l['PM10']) + u"("+self.AQI_level_str(l['PM10'])+u")\n" )
            string += ( u"PM25:" + str(l['PM25']) + u"("+self.AQI_level_str(l['PM25'])+u")" )

            return string
        except BaseException as e:
            print e.message
            self.log.update(u"error occur in make_city_desc." + e.message)
