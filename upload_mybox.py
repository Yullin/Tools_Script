#!/user/bin/env python3

import sys, requests, json
from datetime import datetime

ServerIP = sys.argv[1]
URL = "http://" + ServerIP
upfilePath = sys.argv[2]

def get_list():
    url = URL + "/list"
    payload = {'path':'/'}
    html = requests.get(url, params=payload)
    return html.text

def del_file(filename):
    url = URL + "/delete"
    payload = {'path': filename}
    html = requests.post(url, data=payload)
    return html.status_code

def upload_file(filepath):
    url = URL + "/upload"
    dt_str = datetime.now().strftime("%Y%m%d")
    filename = filepath.split('/')[-1]
    filename = dt_str + "-" + filename
    files = {
        "path":(None, '/'),
        "files[]":(filename, open(filepath, 'rb'), "application/octet-stream")
    }
    headers = {
        "Host": ServerIP,
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50",
        "Origin": "http://" + ServerIP,
        "Referer": "http://" + ServerIP + "/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    res = requests.post(url, headers=headers, files=files)
    print("Upload Result: ", res.status_code)

def main():
    res = get_list()
    j_res = json.loads(res)
    for i in j_res:
        print("name:", i['name'])
 
    upload_file(upfilePath)

if __name__ == "__main__":
    main()

# print("arg1:", sys.argv[1])

