#!/usr/bin/env python

# Copyright 2017, Dell EMC, Inc.
# -*- coding: UTF-8 -*-

"""
    Local utilities
"""

def parse_unknown_node_args(unknown_args, known_args):
    """
    parse unknown arguments for node
    """
    if len(unknown_args) == 2:
        known_args.identity = unknown_args[1]
    elif len(unknown_args) > 2:
        raise Exception("unrecognized arguments: {}".format(unknown_args))
    if known_args.opr:
        known_args.subopr = known_args.opr
    known_args.opr = 'nodes'
    return known_args

def parse_unknown_install_args():
    """
    parse unknown arguments for node
    """

def parse_unknown_service_args():
    """
    parse unknown arguments for node
    """

def parse_unknown_test_args():
    """
    parse unknown arguments for node
    """

def parse_all_known(known_args):
    """
    parse unknown arguments for node
    """
    known_args.method = (known_args.method or 'GET').lower()
    if known_args.graph:
        known_args.opr = 'workflows'
        graph = known_args.graph
        if graph.startswith('Graph'):
            graph = '.'.join(graph.split('.')[1:])
    if known_args.pack:
        known_args.opr = 'skus'
    if known_args.method in ['GET', 'DELETE']:
        known_args.header = None
    if known_args.header:
        known_args.header = '{{"content-type": "{}"}}'.format(known_args.header)
