#!/usr/bin/env python3

import subprocess, requests
from logger_class import Logger

ADDR="https://example.com/sendkey"

AlertTitle="VM SSH Login"
AlertContent="Login Message: \n"
LogPath = "/var/log/monit_ssh.log"

def get_login_addr():
    cmd = ['/bin/last']
    res = subprocess.run(cmd)
    ret = res.stdout.split('\n')[:2]
    return '\n'.join(ret)

def send_alert(message):
    m_log = Logger(logger_name='ssh_logger', filename = LogPath )
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    msg = AlertContent + message
    payload = {'text': AlertTitle, 'desp': msg}
    try:
        resp = requests.post(ADDR, data=payload, headers=headers)
    except requests.exceptions.RequestException as e:
        m_log.info("send log failed: %s" %payload)
        m_log.info("send failed reason: %s" %e)

if __name__ == '__main__':
    msg = get_login_addr()
    send_alert(msg)