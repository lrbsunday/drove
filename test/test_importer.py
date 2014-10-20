#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
import unittest
from drove.importer import Importer

class TestImporter(unittest.TestCase):

    def test_importer_default(self):
        """Testing Importer: from standard library"""
        importer = Importer("drove.data")
        cl = importer("value", "test", 1.0)
        assert cl.__class__.__name__ == 'Value'


    def test_importer_path(self):
        """Testing Importer: from path"""
        path = os.path.join(os.path.dirname(__file__), "importer")
        importer = Importer(path=[path], class_suffix="Plugin")
        cl = importer("cpu", None, None)
        assert cl.__class__.__name__ == 'CpuPlugin'
        del sys.modules["cpu"]  # ensure that plugin is removed


    def test_imported_noargs(self):
        """Testing Importer: missing arguments"""
        with self.assertRaises(ImportError):
            Importer()
