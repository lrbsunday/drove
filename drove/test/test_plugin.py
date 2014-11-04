#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import unittest

from drove.config import Config
from drove.channel import Channel
import drove.plugin


class _Mock_tread(object):
    def stop(self, *args, **kwargs):
        pass


class TestingPlugin(drove.plugin.Plugin):
    plugin_name = "test"

    def read(self):
        self.emit(None)

    def write(self, channel):
        assert channel.__class__.__name__ == "Channel"

    def start(self):
        self.read_thread = _Mock_tread()
        self.write_thread = _Mock_tread()


class TestingFailedPlugin(drove.plugin.Plugin):
    plugin_name = "test"

    def read(self):
        raise Exception

    def write(self, channel):
        raise Exception

    def _mock_log(self, *args, **kwargs):
        raise AssertionError


class TestingStartPlugin(drove.plugin.Plugin):
    plugin_name = "test"
    value = []

    def read(self):
        self.value.append("read")

    def write(self, channel):
        self.value.append("write")


class TestPlugin(unittest.TestCase):
    def test_plugin_load(self):
        """testing plugin: load()"""
        config = Config()
        path = os.path.join(os.path.dirname(__file__), "plugin")
        config["plugin_dir"] = [path]
        channel = Channel()
        channel.subscribe("test")
        x = drove.plugin.Plugin.load("sample.cpu", config, channel)
        assert x.__class__.__name__ == "CpuPlugin"

    def test_plugin_load_failed(self):
        """testing plugin: load() (failed)"""
        config = Config()
        path = os.path.join(os.path.dirname(__file__), "plugin")
        config["plugin_dir"] = [path]
        channel = Channel()
        channel.subscribe("test")
        with self.assertRaises(AttributeError):
            drove.plugin.Plugin.load("sample.bad", config, channel)

    def test_plugin_rw(self):
        """Testing Plugin: read() and write()"""
        config = Config()
        channel = Channel()
        channel.subscribe("test")

        x = TestingPlugin(config, channel)
        x.setup(config)
        x._read()
        x._write()

    def test_plugin_stop(self):
        """Testing Plugin: stop()"""
        config = Config()
        channel = Channel()

        x = TestingPlugin(config, channel)
        x.setup(config)
        x.stop()

    def test_plugin_failed(self):
        """Testing Plugin: failing"""
        config = Config()
        channel = Channel()

        x = TestingFailedPlugin(config, channel)
        x.setup(config)
        x.log.error = x._mock_log

        with self.assertRaises(AssertionError):
            x._read()

        with self.assertRaises(AssertionError):
            x._write()

    def test_plugin_start(self):
        """Testing Plugin: start() with handlers"""

        config = Config()
        channel = Channel()
        config["read_interval"] = 0
        config["write_interval"] = 0
        channel.subscribe("test")

        with self.assertRaises(AssertionError):
            x = TestingStartPlugin(config, channel)
            x.start()
            assert "read" in x.value
            assert "write" in x.value

    def test_plugin_manager_loop(self):
        """Testing PluginManager: waiting loop"""
        config = Config()
        channel = Channel()
        x = drove.plugin.PluginManager(config, channel)
        x.loop(1000, 0)

    def test_plugin_manager(self):
        """Testing PluginManager: basic behaviour"""

        config = Config()
        channel = Channel()
        config["read_interval"] = 0
        config["write_interval"] = 0
        path = os.path.join(os.path.dirname(__file__), "plugin")
        config["plugin_dir"] = [path]
        config["plugin.sample.cpu"] = True
        channel.subscribe("test")

        x = drove.plugin.PluginManager(config, channel)
        assert x.plugins[0].__class__.__name__ == "CpuPlugin"
        x.plugins = [TestingPlugin(config, channel)]
        x.start_all()
        assert len(x) == 1
        assert len([i for i in x]) == 1
        x.stop_all()
