
try:
    import tweepy350 as tweepy
except:
    import tweepy

import aqiLog
import random



class _tweet:
    consumer_key="---------------------------------------------------"
    consumer_secret= "---------------------------------------------------"
    access_token="---------------------------------------------------"
    access_token_secret="---------------------------------------------------"

    api = -1

    def __init__(self, where = ""):
        self.log = aqiLog._log( where )


    def init(self):
        try:                
            auth = tweepy.auth.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            auth.secure = True
            self.api = tweepy.API(auth)
            self.log.update(u"initializing _tweet success")
            return True
        except:
            self.log.update(u"initializing _tweet failed")
            return False

    def send_status(self,string,reply_id=0):
        if self.api == -1:
            self.init()

        try:
            if reply_id==0:
                obj =  self.api.update_status(status=(string).encode('utf-8'))
            else:
                obj =  self.api.update_status(status=(string).encode('utf-8'),in_reply_to_status_id=reply_id)
            return obj
        except tweepy.error.TweepError as e:
            self.log.update(u"error occur in send_status. {0}".format(e[0][0][u'message']))
            self.log.update(u"failed messge = {0}".format(string))
            return False

    def sendStatus(self,string,reply_id=0):
        return self.send_status(string,reply_id)

    def send_random_string(self):
        string = ""
        for i in range(20):
            string = string + str(random.randrange(0,10))
        string = u"@null " + string
        obj =  self.api.update_status(status=string.encode('utf-8'))
        self.api.destroy_status(obj.id)

    def sendRandomString(self):
        self.send_random_string()

    def get_api(self):
        if self.api == -1:
            self.init()
        return self.api

    def getAPI(self):
        return self.get_api()

    def send_status_with_media(self,path,string,reply_id=0):
        if self.api == -1:
            self.init()
        try:

            media_id_list = []
            media_id_list.append( self.upload_media(path) )
            
            if reply_id==0:
                obj =  self.api.update_status(status=(string).encode('utf-8'),media_ids = media_id_list)
            else:
                obj =  self.api.update_status(status=(string).encode('utf-8'),in_reply_to_status_id=reply_id,media_ids = media_id_list)
                
            return obj
        except tweepy.error.TweepError as e:
            self.log.update(u"error occur in send_status_with_media. {0}".format(e[0][0][u'message']))
            return False

    def upload_media(self, filename):
        if self.api == -1:
            self.init()
        try:
            media_id = self.api.media_upload(filename).media_id
        except tweepy.error.TweepError as e:
            self.log.update(u"error occur in upload_media. {0}".format(e[0][0][u'message']))
            return False
        return media_id
