#!/usr/bin/env python

# Copyright 2017, Dell EMC, Inc.
# -*- coding: UTF-8 -*-

"""
    Test utilities for RackHD built-in self-test script.
    This file packs frequently used functions and classes for RackHD BIST
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
    Get BIST configurations from configure files
    """
    rackhd_bist_config = robust_load_json_file("./bist_rackhd_config.json")
    if rackhd_bist_config["exit_code"]:
        print rackhd_bist_config["message"]
        sys.exit(-1)
    user_bist_config = robust_load_json_file("./bist_user_config.json")
    if user_bist_config["exit_code"]:
        print user_bist_config["message"]
        sys.exit(-1)

    #user_bist_config can override rackhd_bist_config
    return dict(rackhd_bist_config["message"], **user_bist_config["message"])

def robust_load_json_file(path):
    """
    Load json file by given file path without breaking test
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
    Open file by given file path without break test
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

def initiate_logger(name, path):
    """
    Initiate bist test logging configures
    Logs will be stored in log file as well output to console
    :param name: logger name
    :param path: log file path
    :return logger: python logger object with two handlers
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    time_string = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    if not os.path.exists(path):
        os.mkdir(path)
    logfile_name = os.path.join(path, "rackhd_bist_{}.log".format(time_string))
    logfile = logging.FileHandler(logfile_name)
    console = logging.StreamHandler()
    logfile.setLevel(logging.DEBUG)  # Log file will record all messages
    console.setLevel(logging.DEBUG)  # Console will report WARNNING and ERROR
    formatter = logging.Formatter(
        '[%(levelname)-7s][%(asctime)-15s] %(message)s'
    )
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)
    logger.addHandler(console)
    return logger

def tool_version_compare(version_a, version_b):
    """
    Compare for tool version:
    :param version_a: version to be compared
    :param version_b: version to be compared
    :return  1: version_a is larger than version_b
             0: version_a equals version b
            -1: version-a is smaller than version b
            -2: input parameters include empty value
    """
    if not version_a or not version_b:
        return -2
    version_a_bits = version_a.split(".")
    version_b_bits = version_b.split(".")
    if version_a_bits > version_b_bits:
        return 1
    elif version_a_bits < version_b_bits:
        return -1
    else:
        return 0

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

CONFIGURATION = get_configurations()

class Logger(object):
    """
    RackHD BIST specified logging class
    """
    def __init__(self):
        self.name = "rackhd_bist_log"
        self.path = os.path.join(os.getcwd(), "log/")
        self.logger = initiate_logger(self.name, self.path)
        self.indent = "  "
        self.details_indent = "    "
        self.colored_headers = {
            "warning": "\033[93m" + self.indent + u'\u2717'.encode('utf8') + " ", # yellow
            "error": "\033[91m" + self.indent + u'\u2718'.encode('utf8') + " ", # red
            "debug": "\033[92m" + self.indent + u'\u2713'.encode('utf8') + " ", # green
            "info": "\033[92m" + self.indent + '-' + " ", # green
            "details": "\033[90m" + self.details_indent, # grey
            "title": "\033[1m", # bold
            "end": "\033[0m" # end
        }

    def print_test_suite_name(self, name):
        """
        Print class name
        """
        log_message = '{0}{1}{2}'.format(
            self.colored_headers["title"], name, self.colored_headers["end"])
        print log_message

    def create_colored_log(self, log, color):
        """
        Print class name
        """
        colored_log = '{0}{1}{2}'.format(color, log, self.colored_headers["end"])
        return colored_log

    def record_log_message(self, description, level, details):
        """
        Record RackHD BIST log message in a unified format
        :param description: short log description for a test, required
        :param details: detailed information for a test, optional
        :param level: logging level, one of ["debug", "info", "warning", "error" ]
        """
        assert level in ["info", "warning", "error", "debug"], "Logging level is incorrect"
        assert isinstance(description, str), "Log description should be a string"
        #log_message = self.description_indent + description  # 2 space indent
        log_message = description  # 2 space indent
        if details:
            if level == "warning" or level == "error":
                #details = self.details_indent + details  # 4 space indents
                details = self.create_colored_log(details, self.colored_headers["details"])
                log_message = log_message + "\n" + details
            else:
                log_message = log_message + ": " + details
        log_message = self.create_colored_log(log_message, self.colored_headers[level])
        logger_method = getattr(self.logger, level)
        logger_method(log_message)

    def record_command_result(self, description, level, status):
        """
        Logging according command output
        :param status: return of robust_check_output, robust_open_file or robust_load_json_file,
            an example:
            {"exit_code": 0, "message": "check_call command succeeded"}
        :param description: short log description for a test
        :param level: logging level if test failed
        """
        details = status["message"].strip("\n")
        if status["exit_code"] == 0:
            level = 'debug'
            #description = description + " succeeded"
        else:
            description = description + " failed"
        self.record_log_message(description, level, details)
