

import time
import os
FOR_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class _strTime:



    def intToStr(self,i):
        if i<10:
            return '0'+str(i)
        else :
            return ''+str(i)

    def today(self):
        timeList = []
        timeList.append( time.localtime().tm_year )
        timeList.append( time.localtime().tm_mon )
        timeList.append( time.localtime().tm_mday )

        string = u''
        for i in range(3):
            string += self.intToStr( timeList[i] )
        return string
        
    def now(self):

        timeList = []
        timeList.append( time.localtime().tm_hour )
        timeList.append( time.localtime().tm_min )
        timeList.append( time.localtime().tm_sec )
        
        string = u'['
        for i in range(3):
            string += self.intToStr( timeList[i] )
            if i != 2:
                string += u':'
            else:
                string += u'] '
        return string
        
class _log:
    def __init__(self, location = ""):
        FOR_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.default_path = FOR_DIR + "/log/" + location +"/"
        self.str_time = _strTime()

    def update(self, string):
        today = self.str_time.today()
        now = self.str_time.now()
        
        if type(string) == type('str'):
            string = string.decode('utf8')
        
        string = string.replace('\n',' ')
        s = now + string + '\n'
    
        file_path = self.default_path + today +'.txt'

        try:
            if os.path.exists( file_path ):
                f = open( file_path, 'a' )
            else:
                f = open( file_path, 'w' )
            f.write( s.encode('utf8') )
            f.close()
            
        except BaseException as e:
            err = open(FOR_DIR+'/log/FAILED.txt','a')
            err.write( "["+today+"] "+ now + e.message )
            err.close()
	    
        

def update(string, folder=""):

    str_time = _strTime()
    today = str_time.today()
    now = str_time.now()

    if folder != "":
        folder = folder + "/"
        
    if type(string) == type('str'):
        string = string.decode('utf8')
        
    string = string.replace('\n',' ')
    s = now + string + '\n'

    
    file_path = FOR_DIR+'/log/'+ folder + today +'.txt'

    try:
        if os.path.exists( file_path ):
            f = open( file_path, 'a' )
        else:
            f = open( file_path, 'w' )
            
        f.write( s.encode('utf8') )
        f.close()
        return
            
    except BaseException as e:
        f = open(FOR_DIR+'/log/FAILED.txt','a')
        f.write( "["+today+"] "+ now + e.message )
        f.close()
        return
