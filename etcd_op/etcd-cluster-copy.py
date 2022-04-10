#!/usr/bin/env python3
import etcd3, json, sys
import os.path as os_path

username = ""
passwd = ""
key_prefix = "/apisix/"
Record_Ptr = "Only" #True, Only, False

#def init_etcd(host_addr):
#    etcd = etcd3.client(host=host_addr, port=2379, user=username, password=passwd, grpc_options={
#                        'grpc.http2.true_binary': 1,
#                        'grpc.http2.max_pings_without_data': 0,
#                    }.items())
#    return etcd

def init_etcd(host_addr):
    etcd = etcd3.client(host=host_addr, port=2379, grpc_options={
                        'grpc.http2.true_binary': 1,
                        'grpc.http2.max_pings_without_data': 0,
                    }.items())
    return etcd

def slash_domain(domain):
    tmp_lst = domain.split('.')
    tmp_lst.reverse()
    return '/'.join(tmp_lst)

def dot_domain(domain):
    tmp_lst = domain.split('/')
    tmp_lst.reverse()
    return '.'.join(tmp_lst)

def search_key(etcd_client, keyname):
    result = etcd_client.get(keyname)
    return result

def search_prefix(etcd_client, keyname):
    result = etcd_client.get_prefix(keyname)
    return result

def put_key(etcd_client, keyname, value):
    result = etcd_client.put(keyname, value)
    return result

def check_key(etcd_client, keyname):
    record, _ = search_key(etcd_client, keyname)
    if record:
        return True
    else:
        return False


if __name__ == '__main__':
    #zonename = sys.argv[1]
    key = sys.argv[1]
    etcd_s = init_etcd("10.2.1.101")   #source etcd
    etcd_d = init_etcd("10.2.1.40")   #destination etcd
    full_key = os_path.join(key_prefix, key)
    print("full key:", full_key)
    res = search_prefix(etcd_s, full_key)
    for record, domain in res:
        key_name = domain.key.decode()
        #dom = dot_domain(dom[9:])
        value = record.decode()
        print("key: {}, value: {}".format(key_name, value))
        put_key(etcd_d, key_name, value)
        #print(record.decode())
