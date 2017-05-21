#!/usr/bin/env python

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
    header = options['header'] or {'content-type': 'applicaton/json'}
    if header == {'content-type': 'applicaton/json'}:
        data = json.dumps(options['payload'])
    req = requests.post(url=options['url'], data=data, header=header)
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

def http_put(url, data, header):
    '''
    implement http DELETE.
    :param url: http url link
    '''
    header = options['header'] or {'content-type': 'applicaton/json'}
    if header == {'content-type': 'applicaton/json'}:
        data = json.dumps(options['payload'])
    req = requests.put(url=url, data=data, header=header)
    return req

def http_patch(url, data, header):
    '''
    implement http DELETE.
    :param url: http url link
    '''
    header = options['header'] or {'content-type': 'applicaton/json'}
    if header == {'content-type': 'applicaton/json'}:
        data = json.dumps(options['payload'])
    req = requests.patch(url=url, data=data, header=header)
    return req
