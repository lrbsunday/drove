#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import sys
import unittest
from drove.util import temp


class TestTemp(unittest.TestCase):

    def _mock_flush(*args, **kwargs):
        pass

    def test_temp_variable(self):
        """Testing util.temp.variables: basic behaviour"""
        with temp.variables({"sys.argv": ['test_value']}):
            assert sys.argv[0] == 'test_value'
        assert sys.argv[0] != 'test_value'

        with temp.variables({"sys.stdout.flush": self._mock_flush}):
            assert sys.stdout.flush == self._mock_flush

        with self.assertRaises(ValueError):
            with temp.variables({"fail": None}):
                pass
