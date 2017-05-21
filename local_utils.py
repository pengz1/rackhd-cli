#!/usr/bin/env python

# Copyright 2017, Dell EMC, Inc.
# -*- coding: UTF-8 -*-

"""
    Local utilities
"""

import os
import sys
import re
import json
import time
import subprocess
import logging

def get_configurations():
    """
    Get configurations from configure files
    """
    # configure file should be under command executing path
    path = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(path, "config.json")
    rackhd_bist_config = robust_load_json_file(path)
    if rackhd_bist_config["exit_code"]:
        print rackhd_bist_config["message"]
        sys.exit(-1)
    return rackhd_bist_config["message"]

def robust_load_json_file(path):
    """
    Load json file by given file path
    :param path: full file path like "/home/onrack/src/test.json"
    :return: a dict includes exit_code and message, an example:
        {"exit_code": 0, "message": {"config_a": 0, "config_b": 1}}
        message is a json object if loaded json file successfully
    """
    exit_status = {}
    try:
        with open(path) as data_file:
            json_obj = json.load(data_file)
    except IOError:
        exit_status["exit_code"] = -1
        exit_status["message"] = "Can't find or unable to access {}".format(path)
    except ValueError:
        exit_status["exit_code"] = -1
        exit_status["message"] = "Can't load {}, json format is required".format(path)
    else:
        exit_status["exit_code"] = 0
        exit_status["message"] = json_obj
    return exit_status

def robust_check_output(cmd, shell=False, redirect=False,):
    """
    Subprocess check_output module with try-except to catch CalledProcessError and OSError
    :param cmd: command option for subprocess.check_output
    :param redirect: a flag to decide if STDERR should be re-directed to STDOUT
    :return: a dict include exit_code and message, an example:
        {"exit_code": 0, "message": "check_call command succeeded"}
        message is the output string of a command if command succeeded
    """
    exit_status = {"exit_code": 0, "message": ""}
    try:
        if redirect:
            output = subprocess.check_output(cmd, shell=shell, stderr=subprocess.STDOUT)
        else:
            output = subprocess.check_output(cmd, shell=shell)
    except subprocess.CalledProcessError as err:
        exit_status["message"] = err.output
        exit_status["exit_code"] = err.returncode

    #In redirect mode, subprocess will report OSError if command can't be found
    except OSError as err:
        exit_status["message"] = str(err)
        exit_status["exit_code"] = -1
    else:
        exit_status["message"] = output
    return exit_status

def robust_open_file(path):
    """
    Open file by given file path with try-catch
    :param path: full file path like "/home/onrack/src/test.py"
    :return: a dict includes exit_code and message, an example:
        {"exit_code": 0, "message": [...]}
        message is a list contains file.readlines() return if file opened successfully
    """
    exit_status = {"exit_code": 0, "message": "check_call command succeeded"}
    try:
        with open(path) as data_file:
            lines = data_file.readlines()
    except IOError:
        exit_status["message"] = "Can't find or access file {}".format(path)
        exit_status["exit_code"] = -1
    else:
        exit_status["message"] = lines
    return exit_status

def get_tool_version(cmd, redirect=False):
    """
    Use given command to get tool version
    :param cmd: command to get tool version
    :param redirect: flag decide if we should redirect STDERR to STDOUT
    :return: tool version string
    """
    result = robust_check_output(cmd=cmd, shell=False, redirect=redirect)
    pattern = re.compile(r'\d\.(\d\.)*\d')
    if result["exit_code"] == 0:
        version = pattern.search(result["message"])
        if version:
            result["message"] = version.group(0) ## refine output message
        else:
            result["exit_code"] = -1
            result["message"] = "Failed to get version with command [{}]".format(",".join(cmd))
    return result

def create_rackhd_api(option):
    """
    Use given command to get tool version
    :param cmd: command to get tool version
    :param redirect: flag decide if we should redirect STDERR to STDOUT
    :return: tool version string
    """
    method = option["method"]
    content_type = ""
    if method != 'GET':
        content_type = '-H "content-type: {}"'.format(option["content-type"])
    url = option["url"]["protocol"] + "://" + option["url"]["server"] + ":" + option["url"]["port"]
    api_option = option["api"]
    for key, value in enumerate(api_option):
        if value:
            api_option[key] = "/" + value
    api = "/api" + api_option["version"] + api_option["opr"] + api_option["id"] + api_option["subopr"]
    param = option["param"]
    payload = "-d \'" + json.dumps(option["payload"]) + "\'"
    command = "curl -X {0} {1} {2}{3}{4} {5} ".format(method, content_type, url, api, param, payload)
    return command

CONFIGURATION = get_configurations()
