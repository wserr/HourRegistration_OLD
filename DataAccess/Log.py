import logging
import configparser

'''
Simple logging class
To use in project: import Log
Log.Logger.LogInfo('***')
'''

class Logger(object):
    config = configparser.ConfigParser()
    config.read('config.ini')
    # create logger 
    logger = logging.getLogger(config['LOGGING']['Name'])
    logger.setLevel(int(config['LOGGING']['LoggingLevel']))
    # create file handler which logs even debug messages
    fh = logging.FileHandler(config['LOGGING']['Path'] + config['LOGGING']['Name'] + '.log')
    fh.setLevel(int(config['LOGGING']['LoggingLevel']))
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


     
    #define methods for logging
    def LogInfo(mess):
        Logger.logger.info(mess + '\n')
        
    def LogWarning(mess):
        Logger.logger.warning(mess + '\n')
        
    def LogError(mess,fatal=False):
        Logger.logger.error(mess + '\n',exc_info=fatal)


        
        
    



