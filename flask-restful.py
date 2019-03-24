#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Danny 2019-03-25
import re
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

ARGS = {
    'system': 'linux',
    'ip': 'xxx.xxx.xxx.254',
    'vlan': 13,
}


def checkip(ip):
	regex = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
	if regex.match(ip):
		return True
	else:
		print "IP is incorrect!"
		return False

def abort_if_args_doesnt_right(args):
    if args['system'] not in ['linux', 'windows']:
        abort(400, message="system {} is not supported".format(args['system']))
    if not checkip(args['ip']):
        abort(400, message="ip {} is invalid".format(args['ip']))


parser = reqparse.RequestParser()
parser.add_argument('system')
parser.add_argument('ip')
parser.add_argument('vlan')


# # 操作（put / get / delete）单一资源Todo
# shows a single todo item and lets you delete a todo item
# class Todo(Resource):
#     def get(self, arg_id):
#         abort_if_todo_doesnt_exist(arg_id)
#         return ARGS[arg_id]

#     def delete(self, arg_id):
#         abort_if_todo_doesnt_exist(arg_id)
#         del ARGS[arg_id]
#         return '', 204

#     def put(self, arg_id):
#         args = parser.parse_args()
#         task = {'task': args['task']}
#         ARGS[arg_id] = task
#         return task, 201


# # 操作（post / get）资源列表TodoList
# shows a list of all todos, and lets you POST to add new tasks
class GeneratVirtualDevice(Resource):
    def get(self):
        return ARGS

    def post(self):
        args = parser.parse_args(strict=True)
        print args
        abort_if_args_doesnt_right(args)
        return args, 200



# 设置路由
api.add_resource(GeneratVirtualDevice, '/vdevice')
# api.add_resource(Todo, '/todos/<arg_id>')

if __name__ == '__main__':
    app.run(debug=True)
