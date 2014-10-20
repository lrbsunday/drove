#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import unittest

import drove.timer
import drove.reloader


class MockObject(object):
    def reload(self):
        pass


class TestReloader(unittest.TestCase):
    def setUp(self):
        self._Timer = drove.reloader.Timer

    def tearDown(self):
        drove.reloader.Timer = self._Timer

    def test_reloader(self):
        """Testing Reloader: basic behaviour"""
        x = drove.reloader.Reloader([MockObject()])
        x.reload()

    def test_reloader_start(self):
        """Testing Reloader: start()"""
        x = drove.reloader.Reloader([MockObject()])
        x.start()
