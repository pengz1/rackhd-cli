#!/usr/bin/env python

# Copyright 2017, Dell EMC, Inc.
# -*- coding: UTF-8 -*-

"""
    Local utilities
"""
import re
from utils.mongo_utils import mongo as mongo

def parse_position_node_args(position_args, known_args):
    """
    parse position arguments for node
    """
    if len(position_args) == 2:
        known_args.identity = position_args[1]
    elif len(position_args) > 2:
        raise Exception("unrecognized arguments: {}".format(position_args))
    if known_args.opr:
        known_args.subopr = known_args.opr
    known_args.opr = 'nodes'
    return known_args

def parse_position_service_args(position_args, known_args):
    """
    parse position arguments for node
    """
    assert len(position_args) <= 1, 'unrecognized positional arguments for service'
    if len(position_args) == 0:
        known_args.services = 'all'
    else:
        known_args.services = position_args[0].split(',')

def parse_position_sku_args(position_args, known_args):
    """
    parse position arguments for node
    """
    if len(position_args) == 2:
        arg = position_args[1]
        if arg.startswith('@'):
            known_args.payload = arg
            known_args.subopr = 'pack'
            known_args.method = 'post'
            if known_args.identity:
                known_args.method = 'put'
        else:
            known_args.identity = position_args[1]
    elif len(position_args) == 3:
        known_args.identity = position_args[1]
        pattern = re.compile('[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}')
        if not pattern.match(known_args.identity):
            raise Exception("unrecognized arguments: {}".format(position_args))
        if position_args[2].startswith('@'):
            known_args.payload = position_args[2]
        else:
            raise Exception("unrecognized arguments: {}".format(position_args))
        known_args.subopr = 'pack'
        known_args.method = 'put'
    elif len(position_args) > 3:
        raise Exception("unrecognized arguments: {}".format(position_args))
    if known_args.opr:
        known_args.subopr = known_args.opr
    known_args.opr = 'skus'
    return known_args

def parse_position_install_args():
    """
    parse position arguments for node
    """

def parse_position_test_args():
    """
    parse position arguments for node
    """

def parse_position_mongo_args(position_args, known_args):
    """
    parse position arguments for mongo identity
    """
    assert len(position_args) == 2, 'unrecognized positional arguments for mongo operation'
    known_args.mongo = position_args[1]

def parse_position_identity_args(position_args, known_args):
    """
    parse position arguments for mongo identity
    """
    assert len(position_args) == 1, 'unrecognized positional arguments for mongo operation'
    collection = mongo.find_collection_by_id(position_args[0])
    if collection == 'workitems':
        known_args.opr = 'pollers'
    else:
        known_args.opr = collection
    known_args.identity = position_args[0]
    known_args.method = 'GET'
    return known_args

def parse_all_known(known_args):
    """
    parse position arguments for node
    """
    known_args.method = known_args.method
    if known_args.cancel:
        known_args.opr = 'nodes'
        known_args.subopr = 'workflows'
        known_args.identity = known_args.cancel
        known_args.param = 'action'
        known_args.payload = '{"command":"cancel"}'
        known_args.method = 'PUT'
        known_args.header = {'content-type': 'application/json'}
        return known_args
    if known_args.mock:
        known_args.opr = 'nodes'
        known_args.subopr = 'workflows'
        known_args.identity = known_args.mock
        known_args.graph = 'Graph.BootstrapUbuntuMocks'
        known_args.method = 'POST'
        known_args.payload = known_args.payload or '{"options":{"bootstrap-ubuntu":{"overlayfsFile": "secure.erase.overlay.cpio.gz"}}}'
        return known_args
    if known_args.delete:
        known_args.opr = mongo.find_collection_by_id(known_args.delete)
        known_args.identity = known_args.delete
        known_args.method = 'DELETE'
        return known_args
    if known_args.active:
        known_args.opr = "nodes"
        known_args.subopr = "workflows"
        known_args.identity = known_args.active
        known_args.query = 'active=true'
        return known_args
    if known_args.identity:
        if not known_args.opr:
            known_args.opr = mongo.find_operator_by_id(known_args.identity)
    if known_args.graph:
        known_args.opr = 'workflows'
        known_args.method = 'POST'
        if not known_args.graph.startswith('Graph'):
            known_args.graph = 'Graph.' + known_args.graph
    if known_args.pack:
        known_args.opr = 'skus'
    if known_args.method in ['GET', 'DELETE']:
        known_args.header = None
    if known_args.header:
        known_args.header = {"content-type": known_args.header}
