#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import unittest
from drove.daemon import Daemon


class TestDaemon(unittest.TestCase):
    def setUp(self):
        if os.name == "posix":
            self._fork = os.fork
            self._kill = os.kill
        else:
            self._fork = None
            self._kill = None

    def tearDown(self):
        if self._fork:
            os.fork = self._fork
        if self._kill:
            os.kill = self._kill

    def test_daemon_posix(self):
        """Testing daemon.posix: parent behaviour"""
        d = Daemon.create(lambda: None, lambda: None)
        d.foreground()
        os.fork = lambda: 0
        d.start()
        d.restart()

    def test_daemon_posix_child(self):
        """Testing daemon.posix: child behaviour"""
        d = Daemon.create(lambda: None, lambda: None)
        os.fork = lambda: 100
        os.kill = lambda x, y: None
        d.start()
        assert d.pid == 100
        d.stop()
        assert d.pid == 0
