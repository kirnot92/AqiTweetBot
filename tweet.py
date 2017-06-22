# -*- coding: cp949 -*-

import time
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/module')
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

import tweetClass
import parserClass
import aqiLog 

tweet = tweetClass._tweet()
log = aqiLog._log()
parser = parserClass._parser()

tweet.init()
hour = time.localtime().tm_hour
minute = time.localtime().tm_min


city_list = ['seoul','busan','incheon','daegu', 'daejeon', 'gwangju']

if __name__ == '__main__':
    log.update("------ START MAIN PROCESS ------")
    reply_id = 0
    try:
        string = u""
        for city in city_list:
            print "about "+city
            desc_str = parser.make_city_desc(city)
            
            if len( string + desc_str ) > 140:
                obj = tweet.send_status( string )
                reply_id = obj.id
                log.update("tweet sended")
                string = "" + desc_str
            else:
                string = string + desc_str
        tweet.send_status( string, reply_id )
        log.update("tweet sended")
    except BaseException as e:
        log.update(u"error occur in main. " + e.message)
    
    

    
