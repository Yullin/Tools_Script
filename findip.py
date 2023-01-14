#!/usr/bin/env python
#-*- coding:utf8-*-

# import urllib2, sys
import re, requests, sys
# from sys import version_info

API_URL = "http://freeapi.ipip.net/"

def welcome():
#     if version_info.major == 2:
#         print '''
#     本脚本使用的是IPIP.net的数据
#     如果要退出，请输入q或者quit
#                  Danny 20180716
# '''
#     else:
    print('''
    本脚本使用的是IPIP.net的数据
    如果要退出，请输入q或者quit
                 Danny 20180716
''')

def check_ip(ip_addr):
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip_addr):
        # print "IP vaild"
        return True
    else:
        # print "IP invaild"
        return False

def get_ip_location(ip_addr):
    req_str = API_URL+ip_addr
    # res = urllib2.urlopen(req_str)
    res = requests.get(req_str)
    for word in str(res.content).split(','):
        # print word.strip(re.match("[]"))
        module = re.compile(r"\[|\]")
        # if version_info.major == 2:
        #     print re.sub(module, "", word)
        # else:
        print("word: {}, module: {}".format(word, module))
        print(re.sub(module, "", word))
    # print res.read()

def main():
    if len(sys.argv) == 1:
        welcome()
        while True:
            input_ip = input('Input IP address: ')
            if input_ip == 'q' or input_ip == 'quit':
                sys.exit()
            check_res = check_ip(input_ip)
            if check_res:
                get_ip_location(input_ip)
            else:
                # if version_info.major == 2:
                #     print "Wrong IP address, Please check!"
                # else:
                print("Wrong IP address, Please check!")
    else:
        check_res = check_ip(sys.argv[1])
        if check_res:
            get_ip_location(sys.argv[1])
        else:
            # if version_info.major == 2:
            #     print "Wrong IP address, Please check!"
            # else:
            print("Wrong IP address, Please check!")

if __name__ == '__main__':
    ip = '8.8.8.8'
    # check_ip(ip)
    main()
