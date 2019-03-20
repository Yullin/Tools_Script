#!/usr/bin/env /opt/ftp_file_watcher/bin/python
#-*- coding: utf-8 -*-

import logging.handlers
 
class Logger(logging.Logger):
    def __init__(self, logger_name = 'logger', filename='catch.log', rotat_when='midnight', interval = 1, backcount = 30 ):
        super(Logger, self).__init__(self)
        # 日志文件名
        # if filename is None:
        #     filename = './logs/pt.log'
        self.name = logger_name
        self.filename = filename
        self.rotat_when = rotat_when
        self.interval = interval
        self.backcount = backcount
 
        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(self.filename, self.rotat_when, self.interval, self.backcount)
        fh.suffix = "%Y%m%d-%H%M.log"
        fh.setLevel(logging.DEBUG) 
 
        # 再创建一个handler，用于输出到控制台 
        # ch = logging.StreamHandler() 
        # ch.setLevel(logging.DEBUG) 
 
        # 定义handler的输出格式 
        # formatter = logging.Formatter('[%(asctime)s] - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s') 
        fmt = "%(asctime)s %(name)s %(levelname)s: %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        logFormatter = logging.Formatter(fmt, datefmt)
        fh.setFormatter(logFormatter) 
        # ch.setFormatter(logFormatter) 
 
        # 给logger添加handler 
        self.addHandler(fh) 
        # self.addHandler(ch)
