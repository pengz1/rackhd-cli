#!/usr/bin/env python

import test_utils as utils

class RackhdServices(object):
    """
    RackHD services test suite
    """
    def __init__(self):
        self.source_code_path = CONFIGURATION.get("sourceCodeRepo")
        self.is_regular_repo = (self.source_code_path == "/var/renasar") or (
            self.source_code_path == "/var/renasar/")
        self.services = CONFIGURATION.get("rackhdServices")
        self.heartbeat_unavailable_flags = self.services[:]
        self.amqp_address = {"host": "localhost", "port": 5672}
        self.amqp_connect_timeout = 20
        self.amqp_connection = {}

    def __get_version_from_dpkg(self, service):
        """
        Check RackHD version from 'dpkg -l' output
        """
        # dpkg -l output example:
        #   ii  on-http 2.0.0-20170316UTC-25c81ec  amd64  RackHD HTTP engine service
        cmd = ["dpkg -l | grep {} | awk '{{print $3}}'".format(service)]
        result = utils.robust_check_output(cmd=cmd, shell=True)
        if not result["message"]:
            result["exit_code"] = -1
        return result

    def __get_version_from_commitstring(self, service):
        """
        Check RackHD version from commitstring.txt file
        """
        commitStringPath = os.path.join(self.source_code_path, service, "commitstring.txt")
        result = utils.robust_open_file(commitStringPath)
        return result

    def __get_version_from_package(self, service):
        """
        Check RackHD version from package.json file
        """
        package_file_path = os.path.join(self.source_code_path, service, "package.json")
        result = utils.robust_load_json_file(package_file_path)
        version = result["message"].get("version")
        if not result["exit_code"] and version:
            result["message"] = version
        return result

    def check_service_version(self):
        """
        Check RackHD version
        """
        for service in self.services:
            description = "Check service {} version".format(service)
            if self.is_regular_repo:
                result = self.__get_version_from_dpkg(service)
                if result["exit_code"]:  # if failed to get version from dpkg, try commitstring
                    result = self.__get_version_from_commitstring(service)
            else:
                result = self.__get_version_from_package(service)
            Logger.record_command_result(description, "warning", result)

    def __operate_regular_rackhd(self, operator):
        """
        Start or stop RackHD services from regular RackHD code repo /var/renasar/
        :param operator: operator for RackHD service, should be "start" or "stop"
        """
        for service in self.services:
            description = "{} RackHD service {}".format(operator.capitalize(), service)
            cmd = ["service", service, operator]
            result = utils.robust_check_output(cmd)
            if not result["exit_code"]:
                result["message"] = ""
            Logger.record_command_result(description, 'error', result)

    def __get_pid_executing_path(self, pid):
        """
        Get Linux pid executing path
        :param pid: Linux process id
        :return: pid executing path string, an example: "/home/onrack/src/on-http"
        """
        # ls -l /proc/<pid> output example
        # lrwxrwxrwx 1 root root   0 Mar 28 14:11 cwd -> /home/onrack/src/on-http
        cmd = ["sudo ls -l /proc/{0} | grep cwd | awk '{{print $NF}}'".format(pid)]
        output = utils.robust_check_output(cmd, shell=True)
        return output["message"].strip("\n")

    def __stop_user_rackhd(self):
        """
        Stop RackHD services from user provided RackHD code repo
        """
        get_pid_cmd = ['ps aux | grep node| grep index.js | sed "/grep/d"| ' \
                            'sed "/sudo/d" | awk \'{print $2}\' | sort -r -n']
        output = utils.robust_check_output(cmd=get_pid_cmd, shell=True)
        process_list = output["message"].strip("\n").split("\n")
        for pid in process_list:
            pid_service_name = self.__get_pid_executing_path(pid).split("/")[-1]
            kill_pid_cmd = ["kill", "-9", pid]
            result = utils.robust_check_output(kill_pid_cmd)
            description = "Stop RackHD service {}".format(pid_service_name)
            Logger.record_command_result(description, 'error', result)

    def __start_user_rackhd(self):
        """
        Start RackHD services from user provided RackHD code repo
        """
        for service in self.services:
            description = "Start RackHD service {}".format(service)
            os.chdir(os.path.join(self.source_code_path, service))
            cmd = ["node index.js > /dev/null 2>&1 &"]  # RackHD services need run in background
            result = utils.robust_check_output(cmd=cmd, shell=True)
            Logger.record_command_result(description, 'error', result)

    def start_rackhd_services(self):
        """
        Start RackHD Services
        """
        if self.is_regular_repo:
            self.__operate_regular_rackhd("start")
        else:
            self.__start_user_rackhd()

    def stop_rackhd_services(self):
        """
        Stop RackHD Services
        """
        if self.is_regular_repo:
            self.__operate_regular_rackhd("stop")
        else:
            self.__stop_user_rackhd()

