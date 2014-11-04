#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
import unittest

from drove.util.importer import load


class TestImporter(unittest.TestCase):

    def test_importer_default(self):
        """Testing importer.load: from standard library"""
        cl = load("drove.data.value", "Value")
        assert cl.__name__ == 'Value'

    def test_importer_path(self):
        """Testing importer.load: from path"""
        path = os.path.join(os.path.dirname(__file__), "importer")
        cl = load("cpu", "CpuPlugin", path=[path])
        assert cl.__name__ == 'CpuPlugin'
        del sys.modules["cpu"]  # ensure that plugin is removed

    def test_importer_module(self):
        """Testing importer.load: module"""
        mod = load("sys")
        assert mod == sys
