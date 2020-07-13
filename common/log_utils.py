import logging
import logstash
import sys
import os
from logging.handlers import RotatingFileHandler

class SingleLineFormatter(logging.Formatter):
    # def formatException(self, exc_info):
    #     result = super().formatException(exc_info)
    #     return repr(result)
 
    def format(self, record):
        result = super().format(record)
        result = result.replace("\n", "\\n")+'\n'
        # if record.exc_text:
        #     result = result.replace("\n", "")
        return result

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
logger.propagate = False
handler = RotatingFileHandler('log/app.log', maxBytes=512*1024*1024, backupCount=2)
# formatter = logging.Formatter('[%(asctime)s] [p%(process)s] [%(funcName)s] [%(pathname)s:%(lineno)d] [%(levelname)s] - %(message)s','%m-%d %H:%M:%S')
formatter = SingleLineFormatter('[%(asctime)s] [p%(process)s] [%(funcName)s] [%(pathname)s:%(lineno)d] [%(levelname)s] - %(message)s','%m-%d %H:%M:%S')
handler.setFormatter(formatter)
handler.terminator = ""
logger.addHandler(handler)

TCP_LOG_ADDR=os.getenv('TCP_LOG_ADDR', '134.209.98.218')
TCP_LOG_PORT=os.getenv('TCP_LOG_PORT', 5500)
TCP_LOG_ENABLE=os.getenv('TCP_LOG_ENABLE', True)
tcp_logger = logging.getLogger('python-logstash-logger')
tcp_logger.setLevel(logging.INFO)
tcp_logger.addHandler(logstash.TCPLogstashHandler(TCP_LOG_ADDR, TCP_LOG_PORT, version=1))
def tcp_log(msg, log_type='info', extra=None):
    try:
        if not TCP_LOG_ENABLE:
            return
        if log_type is 'info':
            tcp_logger.info(msg)
        if log_type is 'error':
            tcp_logger.error(msg)
        if log_type is 'warning':
            tcp_logger.warning(msg)
    except Exception as e:
        print('aaaaa')
        # logger.info(e)
def trace_log():
    import traceback
    just_the_string = traceback.format_exc().replace('\n','!!').replace('\r', '!!!')
    logger.error(just_the_string)