import re

class Regex_Helper:
    def __init__(self):
        pass

    def is_date(self, user_input):
        regex_handler = re.compile('\d\d\/\d\d\/\d\d')
        if(regex_handler.match(user_input) is None):
            return False
        else:
            return True

    def is_ticker(self, user_input):
        regex_handler = re.compile('[A-Z.]{1,6}')
        if(regex_handler.match(user_input) is None):
            return False
        else:
            return True

    def is_time(self, user_input):
        regex_handler = re.compile('\d\d:\d\d:\d\d')
        if(regex_handler.match(ser_input) is None):
            return False
        else:
            return True            
