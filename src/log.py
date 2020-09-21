import logging
from datetime import datetime

class Log_Tool():
    def __init__(self, log_file):
        logging.basicConfig(filename=log_file, filemode="a", level=logging.INFO)

    def start(self, log_title):	
        logger = logging.getLogger(log_title)
        self.start = datetime.now()
        self.start_str = self.start.strftime("%m/%d/%y (%H:%M:%S)")

    def end(self, log_title):
        logger = logging.getLogger(log_title)
        self.end = datetime.now()
        self.end_str = self.end.strftime("%m/%d/%y (%H:%M:%S)") 
        self.results(log_title)
        

    def results(self, log_title):
        logger = logging.getLogger(log_title) 
        total_time = (self.end - self.start).total_seconds()
        total_time = round(total_time, 3)
        total_time = str(total_time) 
        logger.info('Start Time: ' + self.start_str)
        logger.info('End Time: ' + self.end_str)
        logger.info('Elapsed Time was: ' + total_time + ' seconds')        
    
    def error(self, log_title):
        logger = logging.getLogger(log_title)
        time = datetime.now()
        now = time.strftime("%m/%d/%y (%H:%M:%S)")
        logger.info('Error Time: ' + now)
