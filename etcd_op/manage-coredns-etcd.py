#!/usr/bin/env python3
# from prettytable.prettytable import NONE
import etcd3, json, sys
import os.path as os_path
from prettytable import PrettyTable
from absl import app
from absl import flags

from prettytable import DOUBLE_BORDER
from prettytable import FRAME

x = PrettyTable()
username = ""
passwd = ""
key_prefix = "/coredns/"

# etcd.get('/coredns/net/intsig/kylin/y2')
FLAGS = flags.FLAGS
flags.DEFINE_string("put", None, "Add domain name. eg: a.example.net:192.168.32.12")
flags.DEFINE_string("get", None, "Search domain name.")
flags.DEFINE_string("delete", None, "Delete a domain name.")
flags.DEFINE_string("prefix", None, "Prefix path.")

etcd = etcd3.client(host='192.168.32.4', port=2379, user=username, password=passwd, grpc_options={
                        'grpc.http2.true_binary': 1,
                        'grpc.http2.max_pings_without_data': 0,
                    }.items())

def display_all(etcd_client):
    result = etcd_client.get_prefix(key_prefix)
    return result

def search_prefix(etcd_client, keyname):
    result = etcd_client.get_prefix(keyname)
    return result

def search_key(etcd_client, keyname):
    result = etcd_client.get(keyname)
    return result

def put_key(etcd_client, keyname, value):
    result = etcd_client.put(keyname, value)
    return result

def delete_key(etcd_client, keyname):
    result = etcd_client.delete(keyname)
    return result

def slash_domain(domain):
    tmp_lst = domain.split('.')
    tmp_lst.reverse()
    return '/'.join(tmp_lst)

def dot_domain(domain):
    tmp_lst = domain.split('/')
    tmp_lst.reverse()
    return '.'.join(tmp_lst)

def main(argv):
    x.field_names = ["DOMAIN", "RECORD", "TTL"]
    x.align["DOMAIN"] = "r"
    x.set_style(DOUBLE_BORDER)
    x.hrules = FRAME
    del argv
    if FLAGS.get:
        # print(FLAGS.get)
        key_dom = FLAGS.get
        key = slash_domain(key_dom)
        full_key = os_path.join(key_prefix, key)
        res = search_prefix(etcd, full_key)
        for record, domain in res:
            dom = domain.key.decode()
            dom = dot_domain(dom[9:])
            record_arr = json.loads(record.decode('utf-8'))
            x.add_row([dom, record_arr['host'], record_arr['ttl']])
        # record = res[0]
        # dom = res[1]
        # dom = dom.key.decode()
        # dom = dot_domain(dom)
        # record_arr = json.loads(record.decode('utf-8'))
        # x.add_row([key_dom, record_arr['host'], record_arr['ttl']])
        print(x)
    elif FLAGS.put:
        val = FLAGS.put
        val_arr = val.split(':')
        key_name = os_path.join(key_prefix, slash_domain(val_arr[0]))
        record = {"host":val_arr[1], "ttl":300}
        put_key(etcd, key_name, json.dumps(record))
        print(key_name, json.dumps(record))
    elif FLAGS.delete:
        val = FLAGS.delete
        key_name = os_path.join(key_prefix, slash_domain(val))
        delete_key(etcd, key_name)
        print("delete:", key_name)
    else:
        res = display_all(etcd)
        for record, domain in res:
            dom = domain.key.decode()
            dom = dot_domain(dom[9:])
            record_arr = json.loads(record.decode('utf-8'))
            x.add_row([dom, record_arr['host'], record_arr['ttl']])
            # print("record: ",dom)
            # print("record:",record_arr['host'],"domain:",dom)
        print(x)


if __name__ == "__main__":
    app.run(main)
