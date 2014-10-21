#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import unittest
import drove.log
from drove.log import logging


class TestLog(unittest.TestCase):

    def test_log_getdefaultlogger(self):
        """Testing log: getDefaultLogger()"""
        assert drove.log.getDefaultLogger() == logging.getLogger("drove.default")


    def test_log_socket(self):
        """Testing AppLogger: get_syslog_socket()"""
        import sys
        log = drove.log.AppLogger()

        sys.platform = "linux2"
        assert log.get_syslog_socket() == "/dev/log"

        sys.platform = "freebsd"
        assert log.get_syslog_socket() == "/var/run/log"

        sys.platform = "darwin"
        assert log.get_syslog_socket() == "/var/run/syslog"

        sys.platform = "unknown"
        assert log.get_syslog_socket() == "/dev/log"
        del sys


    def test_log_applogger_syslog(self):
        """Testing AppLogger: syslog"""
        log = drove.log.AppLogger(syslog=True)
        assert "SysLogHandler" in [x.__class__.__name__ for x in log.handlers]


    def test_log_applogger_logfile(self):
        """Testing AppLogger: logfile"""
        log = drove.log.AppLogger(logfile="/dev/null")
        assert "RotatingFileHandler" in \
            [x.__class__.__name__ for x in log.handlers]


    def test_log_applogger_console(self):
        """Testing AppLogger: console"""
        log = drove.log.AppLogger(console=True)
        assert "StreamHandler" in \
            [x.__class__.__name__ for x in log.handlers]
