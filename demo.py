#!/usr/bin/env /opt/ftp_file_watcher/bin/python
#-*- coding: utf-8 -*-

from logger_class import Logger

m_log = Logger(logger_name='watcher', filename = 'catche.log' )

m_log.info('test1')
m_log.warn('test warn')
m_log.debug('test debug')