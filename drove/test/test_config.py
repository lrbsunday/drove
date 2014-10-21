#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import unittest
from drove.config import Config
from drove.config import ConfigError


class TestConfig(unittest.TestCase):

    def test_config_basic(self):
        """Testing Config: basic behaviour"""
        c = Config(os.path.join(os.path.dirname(__file__), "config",
                                "basic.yml"))
        assert c["parameter"] is True

    def test_config_multiline(self):
        """Testing Config: multiline"""
        c = Config(os.path.join(os.path.dirname(__file__), "config",
                                "multiline.yml"))
        assert c["multiline"] == "this is a multiline with words"
        assert c["multiline2"] == "this is a tab multiline"

    def test_config_hierarchy(self):
        """Testing Config: hierarchy"""
        c = Config(os.path.join(os.path.dirname(__file__), "config",
                                "basic.yml"))
        assert c.get_childs("plugin") == {"one", "two"}
        assert c.get_childs("plugin.one") == {"value", "othervalue"}
        assert c.get_childs("plugin.two") == {"value", "othervalue"}

    def test_config_include(self):
        """Testing Config: include"""
        c = Config(os.path.join(os.path.dirname(__file__), "config",
                                "include.yml"))
        assert c["included"] is True

    def test_config_reload(self):
        """Testing Config: reload"""
        c = Config(os.path.join(os.path.dirname(__file__), "config",
                                "basic.yml"))
        c["parameter"] = False
        assert c["parameter"] is False
        c.reload()
        assert c["parameter"] is True

    def test_config_error(self):
        """Testing Config: ConfigError"""
        c = Config(os.path.join(os.path.dirname(__file__), "config",
                                "basic.yml"))
        with self.assertRaises(ConfigError):
            c["included"]

    def test_config_default(self):
        """Testing Config: get with default"""
        c = Config()
        assert c.get("none", "value") == "value"
