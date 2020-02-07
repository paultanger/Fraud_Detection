import random
from datetime import datetime

class Happendazzler(): # formerly used thread
    
    def __init__(self):
#        Thread.__init__(self)
        self.__data__=[]
        self.__data_filenames__=sorted(os.listdir('s3_data'))[3:]
        for event in self.__data_filenames__:
            with open('s3_data/{}'.format(event)) as f: 
                self.__data__.append(f.read())
        self.__event__=random.choice(self.__data__)
        self.__current_time__= datetime.utcnow()
    
    def __update_event__(self):
        self.__event__=random.choice(self.__data__)
    
    def event(self):
        td=datetime.utcnow() - self.__current_time__
        if (td.seconds > 45):
            self.__current_time__=datetime.utcnow()
            self.__update_event__()
        return self.__event__