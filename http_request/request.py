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

def request(method, options):
    '''
    Http request with payload
    :options: http options
    '''
    headers = options['header'] or {'content-type': 'application/json'}
    # Without payload, will run request with {'content-type': 'application/json'}
    if not options["payload"]:
        return requests.request(
            method=method,
            url=options['url'],
            headers=headers
        )
    # With payload string, will run request with {'content-type': 'application/json'}
    if not options['payload'].startswith('@'):
        return requests.request(
            method=method,
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
        headers = None
    res = requests.request(
        method=method,
        url=options['url'],
        data=payload,
        headers=headers
    )
    f.close()
    return res

def post(options):
    '''
    implement http POST.
    :param url: http url link
    :param data: data to be post
    :param header: request header
    '''
    return request('post', options)

def get(options):
    '''
    implement http GET.
    :param url: http url link
    '''
    return request('get', options)

def delete(options):
    '''
    implement http DELETE.
    :param url: http url link
    '''
    return request('delete', options)

def put(options):
    '''
    implement http DELETE.
    :param url: http url link
    '''
    return request('put', options)

def patch(options):
    '''
    implement http DELETE.
    :param url: http url link
    '''
    return request('patch', options)
