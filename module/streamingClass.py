try:
    import tweepy350 as tweepy
except:
    import tweepy
import tweetClass
import aqiLog
import commandClass
import time




# --------------------------------------------------------------------------
# global -------------------------------------------------------------------
# --------------------------------------------------------------------------

tweet = tweetClass._tweet("stream")
tweet.init()
API = tweet.get_api()
g_stopped = 0

user_name = API.auth.get_username()

log = aqiLog._log("stream")


class sudoAuthor():
    screen_name = "retta2357"
    id = "none"


class sudoStatus():
    text = "@{0} stop".format(user_name)
    author = sudoAuthor()
    id = "none"



# --------------------------------------------------------------------------
# streaming class ----------------------------------------------------------
# --------------------------------------------------------------------------


class MyStreamListener(tweepy.StreamListener):


    # ----------------------------------------------------------------------
    # global ---------------------------------------------------------------
    # ----------------------------------------------------------------------
    
    command = 0
    
    def reload_command_class(self):
        reload(commandClass)
        self.command = commandClass._command()

    def init_api(self):
        tweet.init()
        API = tweet.get_api()

    def not_my_follower(self, screen_name):
        follow_me = API.show_friendship(source_screen_name="aqi_bot", target_screen_name=screen_name)
        if follow_me:
            return False
        else:
            return True

    def try_to_send(self, reply_string, reply_id):
        try:
            for trial in range(10):

                log.update(u"try to send reply...")
                if tweet.send_status(reply_string, reply_id):
                    log.update(u"send success. \"{0}\"".format(reply_string))
                    return
                else:
                    log.update(u"send random string sequence...")
                    tweet.send_random_string()
                    time.sleep(5)

            log.update(u"send reply failed 10 times.")
            log.update(u"failed "+ reply_string )

        except:
            log.update(u"something wrong happen in try_to_send")

    # ----------------------------------------------------------------------
    # direct message -------------------------------------------------------
    # ----------------------------------------------------------------------

    def on_direct_message(self, status):

        try:

            dm = status.parse(API, status.direct_message)
            dm.sender = status.parse(API, dm.sender)

            if dm.sender.screen_name == user_name:
                return True


            self.reload_command_class()

            reply_string = u"none"
            id = dm.sender.id
            name = dm.sender.screen_name
            text = dm.text

            log.update(u"direct message is arrived \"{0}\", from {1}".format(text, name))
            raw_string = self.command.handle( text, id, name )
            reply_string = raw_string[ raw_string.index(' ')+1 : ]
            #remove "@[SCREEN_NAME] "

            self.init_api()

            log.update(u"try to send reply...")
            tweet.get_api().send_direct_message(screen_name = name ,text = reply_string )
            log.update(u"send success. \"{0}\"".format(reply_string))
            
        except BaseException as e:
            log.update(u"something bad happen in on_direct_message")
            log.update(u"MESSAGE: " + e.message)

        return True

    # ----------------------------------------------------------------------
    # status ---------------------------------------------------------------
    # ----------------------------------------------------------------------

    def on_status(self, status):
        global g_stopped
        if status.author.screen_name == user_name:
            return True
        if status.text.split()[0] != '@{0}'.format(user_name):
            return True


        self.reload_command_class()

        reply_string = u"none"
        reply_id = status.id

        try:
            text = status.text.split()
            id = status.author.id
            name = status.author.screen_name

            if text[1] == "stop" and name == 'retta2357':
                log.update(u"stop command receive. return False")
                g_stopped = 1
                return False

            raw_text = status.text
            text = raw_text[ raw_text.index(' ')+1: ]


            log.update(u"mention is arrived \"{0}\", from {1}".format(status.text, name))
            reply_id = status.id
            reply_string = self.command.handle( text, id, name )

            self.init_api()
            self.try_to_send( reply_string, reply_id )

        except BaseException as e:
            log.update(u"something bad happen in on_status")
            log.update(u"MESSAGE: " + e.message)


        return True

    # ----------------------------------------------------------------------
    # error ----------------------------------------------------------------
    # ----------------------------------------------------------------------

    def on_error(self, status_code):
        print status_code
        global g_stopped
        if status_code == 420:
            log.update(u"[ERROR] get error code 420. stream shutdown.")
            g_stopped = 1
            return False
        else:
            log.update(u"[ERROR] get error code {0}.".format(status_code))


# --------------------------------------------------------------------------
# main ---------------------------------------------------------------------
# --------------------------------------------------------------------------


def main():
    
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=API.auth, listener=myStreamListener)
    myStream.userstream( async = True )
    log.update(u"[MAIN] streaming started")
    print "dd"
    sleep_time = 3570
    while(sleep_time > 0):
        time.sleep(10)
        sleep_time -= 10
        print "ddddd"

        if sleep_time % 600 == 0:
            log.update(u"[MAIN] running...")
        if g_stopped == 1:
            log.update(u"[MAIN] stream outted. program shutdown.")
            break

    s = sudoStatus()
    myStreamListener.on_status(s)

    log.update(u"[MAIN] thread ended normally")

if __name__ == '__main__':

    log.update(u"[MAIN] -------- START MAIN PROCESS ----------")

    try:
        main()
    except BaseException as e:
        log.update("EXCEPTION OCCUR IN MAIN")
        log.update("MESSAGE:{0}".format(e.message))

    log.update(u"[MAIN] --------------------------------------")
