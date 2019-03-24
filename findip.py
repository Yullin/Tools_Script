#!/usr/bin/env python
#-*- coding:utf8-*-

import urllib2, sys
import re

API_URL = "http://freeapi.ipip.net/"

def welcome():
    print '''
    本脚本使用的是IPIP.net的数据
    如果要退出，请输入q或者quit
                 Danny 20180716
'''

def check_ip(ip_addr):
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip_addr):
        # print "IP vaild"
        return True
    else:
        # print "IP invaild"
        return False

def get_ip_location(ip_addr):
    req_str = API_URL+ip_addr
    res = urllib2.urlopen(req_str)
    for word in res.read().split(','):
        # print word.strip(re.match("[]"))
        module = re.compile(r"\[|\]")
        print re.sub(module, "", word)
    # print res.read()

def main():
    if len(sys.argv) == 1:
        welcome()
        while True:
            input_ip = raw_input('Input IP address: ')
            if input_ip == 'q' or input_ip == 'quit':
                sys.exit()
            check_res = check_ip(input_ip)
            if check_res:
                get_ip_location(input_ip)
            else:
                print "Wrong IP address, Please check!"
    else:
        check_res = check_ip(sys.argv[1])
        if check_res:
            get_ip_location(sys.argv[1])
        else:
            print "Wrong IP address, Please check!"

if __name__ == '__main__':
    ip = '8.8.8.8'
    # check_ip(ip)
    main()
