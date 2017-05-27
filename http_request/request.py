#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import json
import requests

#def http_post(url, data, header):
def http_post(options):
    '''
    implement http POST.
    :param url: http url link
    :param data: data to be post
    :param header: request header
    '''
    data = None
    header = options['header'] or {'content-type': 'applicaton/json'}
    if header == {'content-type': 'applicaton/json'} and options['payload']:
        data = json.dumps(options['payload'])
    req = requests.post(url=options['url'], data=data, headers=header)
    return req

def http_get(options):
    '''
    implement http GET.
    :param url: http url link
    '''
    req = requests.get(options['url'])
    return req

def http_delete(options):
    '''
    implement http DELETE.
    :param url: http url link
    '''
    req = requests.delete(options['url'])
    return req

def http_put(options):
    '''
    implement http DELETE.
    :param url: http url link
    '''
    data = None
    header = options['header'] or {'content-type': 'applicaton/json'}
    if header.get('content-type') == 'application/json':
        data = options['payload']
    req = requests.put(url=options['url'], data=data, headers=header)
    return req

def http_patch(options):
    '''
    implement http DELETE.
    :param url: http url link
    '''
    header = options['header'] or {'content-type': 'applicaton/json'}
    if header == {'content-type': 'applicaton/json'}:
        data = json.dumps(options['payload'])
    req = requests.patch(url=options['url'], data=data, header=header)
    return req
