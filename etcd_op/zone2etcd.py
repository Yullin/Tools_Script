#!/usr/bin/env python3
import etcd3, json, sys
import os.path as os_path

username = ""
passwd = ""
key_prefix = "/coredns/"
Record_Ptr = "Only" #True, Only, False

def init_etcd(host_addr):
    etcd = etcd3.client(host=host_addr, port=2379, user=username, password=passwd, grpc_options={
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

def put_key(etcd_client, keyname, value):
    result = etcd_client.put(keyname, value)
    return result

def check_key(etcd_client, keyname):
    record, _ = search_key(etcd_client, keyname)
    if record:
        return True
    else:
        return False

def insert_etcd(key_name, record_value, etcd_client):
    # val = '.'.join([hostname, zonename])
    # key_name = os_path.join(key_prefix, slash_domain(val))
    record = {"host":record_value, "ttl":300}
    put_key(etcd_client, key_name, json.dumps(record))
    print(key_name, json.dumps(record))

def insert_ptr_etcd(key_name, record_value, etcd_client):
    # val = '.'.join([hostname, zonename])
    # key_name = os_path.join(key_prefix, slash_domain(val))
    if Record_Ptr == "Only":
        record = {"host": record_value}
    else:
        record = {"host": record_value, "ttl": 300}
    put_key(etcd_client, key_name, json.dumps(record))
    print(key_name, json.dumps(record))

def make_ptr_key(hostname):
    a = hostname.split('.')
    a.reverse()
    a.append('in-addr.arpa')
    return '.'.join(a)

def format_hostname(hostname, val, zonename):
    if hostname.endswith('.'):
        ptr_domain = make_ptr_key(val)
        domain = '.'.join([hostname.rstrip('.'), zonename])
    else:
        ptr_domain = make_ptr_key(val)
        domain = '.'.join([hostname, zonename])
    return domain, ptr_domain

if __name__ == '__main__':
    zonename = sys.argv[1]
    etcd_c = init_etcd("10.2.2.2")
    if not os_path.exists(zonename):
        print("file not exist!", zonename)
        sys.exit(1)
    else:
        fp = open(zonename, 'r')
        for l in fp.readlines():
            hostname = l.split()[0]
            val = l.split()[3]
            domain, ptr_domain = format_hostname(hostname, val, zonename)
            if Record_Ptr == "Only":
                keyname = os_path.join(key_prefix, slash_domain(ptr_domain))
            else:
                keyname = os_path.join(key_prefix, slash_domain(domain))
            if check_key(etcd_c, keyname):
                print("already there:", keyname)
            else:
                print("new name:", keyname)
                if Record_Ptr == "Only":
                    insert_ptr_etcd(keyname, domain, etcd_c)
                else:
                    insert_etcd(keyname, val, etcd_c)
            # break
