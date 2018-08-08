#!/usr/bin/env python

# -*- coding: UTF-8 -*-

'''
Argument parser
'''

import argparse

def parse_arguments():
    """
    parse arguments
    """
    ARG_PARSER = argparse.ArgumentParser(description='RackHD secure-erase argument')

    #common arguments, lowercase
    ARG_PARSER.add_argument('-ip', action='store',
                            help='specify ip adress')
    ARG_PARSER.add_argument('--min', action='store_true',
                            help='minimum output payload')
    ARG_PARSER.add_argument('-pwd', action='store', default='admin',
                            help='specify password')
    ARG_PARSER.add_argument('-user', action='store', default='admin',
                            help='specify username')
    ARG_PARSER.add_argument('-g', '--graph', action='store', dest='graph',
                            help='specify graph')
    ARG_PARSER.add_argument('--pack', action='store', dest='pack',
                            help='specify sku packs')

    # API settings
    ARG_PARSER.add_argument('-api', action='store', dest='api',
                            help='specify whole api path')
    ARG_PARSER.add_argument('-ver', action='store', default='current',
                            help='specify API version')
    ARG_PARSER.add_argument('-i', '--identity', action='store', dest='identity',
                            help='specify id')
    ARG_PARSER.add_argument('-s', '--suboperator', action='store', dest='subopr',
                            help='specify sub operator')
    ARG_PARSER.add_argument('-o', '--operator', action='store', dest='opr',
                            help='specify operator')
    ARG_PARSER.add_argument('-p', '--payload', action='store',
                            dest='payload', help='specify payload')
    ARG_PARSER.add_argument('-q', '--query', action='store',
                            dest='query', help='specify query')
    ARG_PARSER.add_argument('-P', '--parameter', action='store',
                            dest='param', help='specify parameters')
    ARG_PARSER.add_argument('-H', '--header', action='store', dest='header',
                            #default='application/json',
                            help='specify content-type header')
    #Http configuration, specify http methods
    ARG_PARSER.add_argument('-PU', '--PUT', action='store_const', const='PUT',
                            dest='method', help='HTTP PUT')
    ARG_PARSER.add_argument('-PO', '--POST', action='store_const', const='POST',
                            dest='method', help='HTTP POST')
    ARG_PARSER.add_argument('-PA', '--PATCH', action='store_const', const='PATCH',
                            dest='method', help='HTTP PATCH')
    ARG_PARSER.add_argument('-DE', '--DELETE', action='store_const', const='DELETE',
                            dest='method', help='HTTP DELETE')
    ARG_PARSER.add_argument('-GE', '--GET', action='store_const', const='GET',
                            dest='method', help='HTTP GET')
    ARG_PARSER.add_argument('--method', action='store', dest='method',
                            choices=['GET', 'PUT', 'PATCH', 'GET', 'DELETE'],
                            help='HTTP methods')


    #RackHD GET all API arguments, first two lowercase characters
    ARG_PARSER.add_argument('-co', action='store_const', dest='opr', const='configs',
                            help='Get all configs')
    ARG_PARSER.add_argument('-ca', action='store_const', dest='opr', const='catalogs',
                            help='Get all configs')
    ARG_PARSER.add_argument('-po', action='store_const', dest='opr', const='pollers',
                            help='Get all poller')
    ARG_PARSER.add_argument('-wo', action='store_const', dest='opr', const='workflows',
                            help='Get all workflows/graphs')
    ARG_PARSER.add_argument('-ho', action='store_const', dest='opr', const='hooks',
                            help='Get all hooks')
    ARG_PARSER.add_argument('-no', '-n', action='store_const', dest='opr', const='nodes',
                            help='Get all nodes')
    ARG_PARSER.add_argument('-ro', action='store_const', dest='opr', const='roles',
                            help='Get all roles')
    ARG_PARSER.add_argument('-sc', action='store_const', dest='opr', const='schemas',
                            help='Get all schemas')
    ARG_PARSER.add_argument('-sk', action='store_const', dest='opr', const='skus',
                            help='Get all skus')
    ARG_PARSER.add_argument('-ta', action='store_const', dest='opr', const='tags',
                            help='Get all tags')
    ARG_PARSER.add_argument('-lo', action='store_const', dest='opr', const='lookups',
                            help='Get all tags')
    ARG_PARSER.add_argument('-ob', action='store_const', dest='opr', const='obms',
                            help='Get all obms')
    ARG_PARSER.add_argument('-ib', action='store_const', dest='opr', const='ibms',
                            help='Get all ibms')

    #Frequently used id operations, Get id types from database
    ARG_PARSER.add_argument('--cancel', '-C', action='store', default='',
                            help='delete active workflow via node id')
    ARG_PARSER.add_argument('--delete', '-D', action='store', default='',
                            help='delete id')
    ARG_PARSER.add_argument('--get', '-G', action='store', default='',
                            help='get id')
    ARG_PARSER.add_argument('--mock', '-M', action='store', default='',
                            help='run ubuntu mock workflow')
    ARG_PARSER.add_argument('--discovery', action='store', default='',
                            help='run discovery workflow')
    ARG_PARSER.add_argument('--mongo', action='store', default='',
                            help='run get mongo data by ID')
    ARG_PARSER.add_argument('--active', action='store', default='',
                            help='run get active workflow by nodeId')

    #Service operation
    ARG_PARSER.add_argument('--services', action='store', dest='services',
                            help='RackHD services')
    ARG_PARSER.add_argument('--start', action='store_const', dest='service', const='start',
                            help='start RackHD service')
    ARG_PARSER.add_argument('--stop', action='store_const', dest='service', const='stop',
                            help='stop RackHD operation')
    ARG_PARSER.add_argument('--restart', action='store_const', dest='service', const='restart',
                            help='restart RackHD operation')
    ARG_PARSER.add_argument('--version', action='store_const', dest='service', const='version',
                            help='get RackHD version operation')
    ARG_PARSER.add_argument('--service', action='store', dest='service',
                            choices=['start', 'stop', 'restart', 'version'],
                            help='get RackHD version operation')
    ARG_PARSER.add_argument('--clear', action='store_const', dest='service', const='clear',
                            help='get RackHD version operation')
    # BIST test
    ARG_PARSER.add_argument('-t', action='store', dest='test',
                            help='initiate RackHD BIST test')
    ARG_PARSER.add_argument('--path', action='store_true', dest='path',
                            help='specify RackHD source code path')

    #Log operation
    ARG_PARSER.add_argument('-l', action='store', dest='log',
                            help='initiate RackHD log')

    #RackHD installation

    #RackHD OS install

    #RackHD configure

    #return a tuple with 0: recognized commands namespace and 1: unparsed commands
    #ARG_LIST, ARG_LIST_UNKNOWN = ARG_PARSER.parse_known_args()
    return ARG_PARSER.parse_known_args()
