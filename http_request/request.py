#!/usr/bin/env python
"""
Wrap http request methods
"""
# -*- coding: UTF-8 -*-

import os
import json
import requests

def unicode2str(data):
    '''
    Convert unicode str got from json.load, json.loads to str
    :param data: string or dict data
    '''
    if isinstance(data, dict):
        return {unicode2str(key): unicode2str(value) for key, value in data.iteritems()}
    elif isinstance(data, list):
        return [unicode2str(element) for element in data]
    elif isinstance(data, unicode):
        return data.encode('utf-8')
    else:
        return data

def request(options):
    '''
    Http request with payload
    :options: http options
    '''
    headers = options['header'] or {'content-type': 'application/json'}
    method = options['method'] and options['method'].lower()
    # Without payload, will run request with {'content-type': 'application/json'}
    if not options["payload"]:
        return requests.request(
            method=method or "get",
            url=options['url'],
            headers=headers
        )
    # With payload string, will run request with {'content-type': 'application/json'}
    if not options['payload'].startswith('@'):
        return requests.request(
            method=method or "POST",
            url=options['url'],
            data=options['payload'],
            headers=headers
        )
    filepath = options['payload'][1:]
    if not filepath.startswith('/'):
        filepath = os.getcwd() + '/' + filepath
    # With json payload file, will run request with {'content-type': 'application/json'}
    if options['payload'].endswith('.json'):
        f = open(filepath, 'r')
        payload = json.load(f)
        payload = json.dumps(payload)
    # With non-json payload file, will run request as binary
    else:
        f = open(filepath, 'rb')
        payload = f
        # multipart/form-data requires boundary
        headers = {'content-type': 'application/x-www-form-urlencoded'}

    res = requests.request(
        method=method or "POST",
        url=options['url'],
        data=payload,
        headers=headers
    )
    f.close()
    return res
