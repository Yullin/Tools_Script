#!/usr/bin/env python
#-*- coding: utf-8 -*-

# LOG_FILE = "/var/log/ftp_watcher.log"
# LOG_FILE = "./test.log"

import logging
from logging.handlers import TimedRotatingFileHandler
from config import LOG_FILE    #从配置文件导入日志路径配置

#采用按时间日期来进行轮转
def logger():
    logHandler = TimedRotatingFileHandler(LOG_FILE,when="midnight")
    # fmt = "%(asctime)s %(filename)s %(levelname)s: %(message)s"
    fmt = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    logFormatter = logging.Formatter(fmt, datefmt)
    logHandler.setFormatter( logFormatter )
    logger = logging.getLogger('FTP_WATCHER')
    logger.addHandler( logHandler )
    logger.setLevel( logging.DEBUG )
    return logger
    
if __name__ == "__main__":
    a_logger = logger()
    for k in range(5):
        a_logger.info("Line %d" %  k)
        a_logger.warn("Line warn %d!" %  k)
