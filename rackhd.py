#!/usr/bin/env python

# Copyright 2016, EMC, Inc.

# -*- coding: UTF-8 -*-

"""
This script is to do Secure Erase (SE) on a compute node
Four methods/tools are integrated in this scripts
A log file will be created for each disk to be erased named after disk name, like sdx.log
"""
import sys
import argparse
import rackhd_services

ARG_PARSER = argparse.ArgumentParser(description='RackHD secure-erase argument')

ARG_PARSER.add_argument("-id", action="store", help="specify node id")
ARG_PARSER.add_argument("-ip", action="store", help="specify ip adress")
ARG_PARSER.add_argument("-pwd", action="store", default='admin', help="specify password")
ARG_PARSER.add_argument("-user", action="store", default='admin', help="specify username")
ARG_PARSER.add_argument("-d", action="store", default='{}', help="specify payload")
ARG_PARSER.add_argument("-ct", action="store", default='content-type: application/json',
                        help="specify content-type")
#Http configuration
ARG_PARSER.add_argument("-ver", action="store", default='current', help="specify API version")
ARG_PARSER.add_argument("-PU", "--PUT", action="store_const", const='PUT', dest='method',
                        help="HTTP PUT")
ARG_PARSER.add_argument("-PO", '--POST', action="store_const", const='POST', dest='method',
                        help="HTTP POST")
ARG_PARSER.add_argument("-PA", '--PATCH', action="store_const", const='PATCH', dest='method',
                        help="HTTP PATCH")
ARG_PARSER.add_argument("-DE", '--DELETE', action="store_const", const='DELETE', dest='method',
                        help="HTTP DELETE")
ARG_PARSER.add_argument("-GE", '--GET', action="store_const", const='GET', dest='method',
                        help="HTTP GET")
ARG_PARSER.add_argument('--method', action="store", dest='method',
                        choices=["GET", "PUT", "PATCH", "GET", "DELETE"], default="GET",
                        help="HTTP methods")


#RackHD GET all API arguments
ARG_PARSER.add_argument("-co", action="store_const", dest="get_all_api", const='configs',
                        help="Get all configs")
ARG_PARSER.add_argument("-wo", action="store_const", dest="get_all_api", const='workflows',
                        help="Get all workflows/graphs")
ARG_PARSER.add_argument("-ho", action="store_const", dest='get_all_api', const='hooks',
                        help="Get all hooks")
ARG_PARSER.add_argument("-no", '-n', action="store_const", dest='get_all_api', const='nodes',
                        help="Get all nodes")
ARG_PARSER.add_argument("-ro", action="store_const", dest='get_all_api', const='roles',
                        help="Get all roles")
ARG_PARSER.add_argument("-sc", action="store_const", dest='get_all_api', const='schemas',
                        help="Get all schemas")
ARG_PARSER.add_argument("-sk", '-s', action="store_const", dest='get_all_api', const='skus',
                        help="Get all skus")
ARG_PARSER.add_argument("-ta", action="store_const", dest='get_all_api', const='tags',
                        help="Get all tags")
ARG_PARSER.add_argument("-lo", '-l', action="store_const", dest='get_all_api', const='lookups',
                        help="Get all tags")
ARG_PARSER.add_argument("-ob", action="store_const", dest='get_all_api', const='obms',
                        help="Get all obms")
ARG_PARSER.add_argument("-ib", action="store_const", dest='get_all_api', const='ibms',
                        help="Get all ibms")
ARG_PARSER.add_argument("--get_all_api", action="store", dest='get_all_api',
                        choices=['configs', 'hooks', 'nodes', 'roles', 'schemas', 'skus', 'tags',
                                 'lookups', 'obms', 'ibms', 'catalogs', 'tasks', 'files',
                                 'profiles', 'templates', 'users', 'views', 'workflows'],
                        help="Get all apis")

#Node operation
subparse = ARG_PARSER.add_subparsers(dest='opr_name')
node_arg = subparse.add_parser('node', help='nodes operation command') #Only node also works
node_arg.add_argument('node_id') # -W works, -w can't work as it can match other parameters, --workflow is a must to store this parameters
node_arg.add_argument('-W', '--node_workflow') # -W works, -w can't work as it can match other parameters, --workflow is a must to store this parameters
node_arg.add_argument('-P', '--node_pollers') # -W works, -w can't work as it can match other parameters, --workflow is a must to store this parameters
node_arg.add_argument('-I', '--node_id') # -W works, -w can't work as it can match other parameters, --workflow is a must to store this parameters
node_arg.add_argument('-O', '--node_data') # -W works, -w can't work as it can match other parameters, --workflow is a must to store this parameters
#workflow_arg = subparse.add_parser('workflow', help='workflow operation command')
#workflow_arg.add_argument('-I', '--workflow_id') # -W works, -w can't work as it can match other parameters, --workflow is a must to store this parameters
#workflow_arg.add_argument('-N', '--workflow_name') # -W works, -w can't work as it can match other parameters, --workflow is a must to store this parameters
#node_arg.add_argument('c', action='store', type=str, dest='catalogs',

#RackHD id operators
'''
ARG_PARSER.add_argument("-workflow", action="store", dest='id', help="workflow operation")
ARG_PARSER.add_argument("-catalog", action="store", dest='id', help="catalog operation")
ARG_PARSER.add_argument("-hook", action="store", dest='id', help="hook operation")
ARG_PARSER.add_argument("-poller", action="store", dest='id', help="poller operation")
ARG_PARSER.add_argument("-sku", action="store", dest='id', help="sku operation")
ARG_PARSER.add_argument("-tag", action="store", dest='id', help="tag operation")
ARG_PARSER.add_argument("-obm", action="store", dest='id', help="obm operation")
ARG_PARSER.add_argument("-lookup", action="store", dest='id', help="obm operation")
'''

#Frequently used id operations
#Get id types from database
ARG_PARSER.add_argument("--cancel", "-C", action="store", default='', dest="id",
                        help="delete active workflow via node id")
ARG_PARSER.add_argument("--remove", '-D', action="store", default='', dest="id",
                        help="delete id")
ARG_PARSER.add_argument("--get", '-G', action="store", default='', dest="id",
                        help="get id")
ARG_PARSER.add_argument("--moc", '-M', action="store", default='', dest="id",
                        help="run ubuntu mock workflow")
ARG_PARSER.add_argument("--discovery", action="store", default='', dest="id",
                        help="run discovery workflow")

#Service operation
ARG_PARSER.add_argument("--start", action="store_const", const='start', dest="service",
                        help="start RackHD service")
ARG_PARSER.add_argument("--stop", action="store_const", const='stop', dest="service",
                        help="stop RackHD operation")
ARG_PARSER.add_argument("--restart", action="store_const", const='restart', dest="service",
                        help="restart RackHD operation")
ARG_PARSER.add_argument("--version", action="store_const", const='version', dest="service",
                        help="get RackHD version operation")
ARG_PARSER.add_argument("--service", action="store", dest="service",
                        choices=['start', 'stop', 'restart', 'version'],
                        help="get RackHD version operation")
#Log operation

ARG_LIST = ARG_PARSER.parse_args()
#ARG_LIST = ARG_PARSER.parse_known_args() # return a tuple with 0: recognized commands and 1: unparsed commands

def rackhd_service(service):
    service = service + "_rackhd_services"
    rackhd = rackhd_services.RackhdServices()
    rackhd.getattr(service)()

if __name__ == "__main__":
    #curl -X POST -H "content-type: application/json" \
    #   http://172.31.128.1:9080/api/current/nodes/id/workflows?name=Graph.Discovery -d '{}'
    # {
    #   method: GET,
    #   content-type: application/json,
    #   opr: nodes,
    #   id: xxxxxxxxxxxx,
    #   subopr1: workflows,
    #   subopr2: /action, ## ?name=Graph.Discovery
    #   payload: {"command": "cancel"}
    # }
    rackhd_api_options = {
        'method': 'GET',
        'url': {
            'server': '172.31.128.1',
            'port': '9080',
            'protocol': "http"
        },
        'content-type': None,
        'api': {
            'opr': 'nodes',
            'id': '',
            'subopr': '',
            'ver': 'current'
        },
        'param': '',
        'payload': None
    }

    print sys.argv[:]
    print ARG_LIST

    #if ARG_LIST.service:
    #    rackhd_service(ARG_LIST.service)
