#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
import unittest
import drove.drove as script


class TestScript(unittest.TestCase):

    def setUp(self):
        self._fork = os.fork
        self._reloader_start = script.drove.reloader.Reloader.start
        self._pluginmanager_loop = script.drove.plugin.PluginManager.loop
        self._path = sys.path

    def tearDown(self):
        sys.argv = ["prog"]
        os.fork = self._fork
        script.drove.reloader.Reloader.start = self._reloader_start
        script.drove.plugin.PluginManager.loop = self._pluginmanager_loop
        sys.path = self._path

    def test_script_flags(self):
        """Testing script: main flags"""
        sys.argv = ["prog", "-np", "-v", "-f"]
        with self.assertRaises(SystemExit) as cm:
            script.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_script_config(self):
        """Testing script: -C flag"""
        sys.argv = ["prog", "-np", "-f", "-C", "./test/config/empty.yml"]
        with self.assertRaises(SystemExit) as cm:
            script.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_script_config_default(self):
        """Testing script: default config"""
        sys.argv = ["prog", "-np", "-f"]
        config = script.DEFAULT_CONFIG_FILES
        script.DEFAULT_CONFIG_FILES = ["./test/config/empty.yml"]
        with self.assertRaises(SystemExit) as cm:
            script.main()
        script.DEFAULT_CONFIG_FILES = config
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_script_environment_ok(self):
        """Testing script: -s flag with fine parameters"""
        sys.argv = ["prog", "-np", "-f", "-s key=value"]
        with self.assertRaises(SystemExit) as cm:
            script.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_script_environment_fail(self):
        """Testing script: -s flag with fine parameters"""
        sys.argv = ["prog", "-np", "-f", "-s key"]
        with self.assertRaises(SystemExit) as cm:
            script.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 2)

    def test_script_exit_handler(self):
        """Testing script: exit_handler"""
        class _Log(object):
            def error(*args, **kwargs):
                return

        class _Plugins(object):
            def stop_all(*args, **kwargs):
                return

        with self.assertRaises(SystemExit) as cm:
            script._exit_handler(_Log(), _Plugins())
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 15)

    def test_script_daemon(self):
        """Testing script: daemon"""
        sys.argv = ["prog"]
        os.fork = lambda: 0
        script.drove.reloader.Reloader.start = lambda x: None
        script.drove.plugin.PluginManager.loop = lambda x: None
        script.main()

    def test_script_daemon_foreground(self):
        """Testing script: daemon (-f)"""
        sys.argv = ["prog", "-f"]
        os.fork = lambda: 0
        script.drove.reloader.Reloader.start = lambda x: None
        script.drove.plugin.PluginManager.loop = lambda x: None
        script.main()

    def test_script_daemon_interrupt(self):
        """Testing script: daemon with KeyboardInterrupt"""
        sys.argv = ["prog"]
        os.fork = lambda: 0

        def _interrupt(x):
            raise KeyboardInterrupt()

        script.drove.reloader.Reloader.start = lambda x: None
        script.drove.plugin.PluginManager.loop = _interrupt
        with self.assertRaises(SystemExit) as cm:
            script.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 15)

    def test_script_daemon_exception(self):
        """Testing script: daemon with BaseException"""
        sys.argv = ["prog"]
        os.fork = lambda: 0

        def _interrupt(x):
            raise Exception()

        script.drove.reloader.Reloader.start = lambda x: None
        script.drove.plugin.PluginManager.loop = _interrupt
        with self.assertRaises(SystemExit) as cm:
            script.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)

    def test_script_daemon_exception_verbose(self):
        """Testing script: daemon with BaseException (-v)"""
        sys.argv = ["prog", "-v"]
        os.fork = lambda: 0

        def _interrupt(x):
            raise Exception()

        script.drove.reloader.Reloader.start = lambda x: None
        script.drove.plugin.PluginManager.loop = _interrupt
        with self.assertRaises(Exception):
            script.main()

    def test_script_setproctitle(self):
        """Testing script: setproctitle"""
        sys.argv = ["prog", "-v", "-np", "-f"]
        sys.path.insert(0, os.path.dirname(__file__))
        with self.assertRaises(ValueError) as cm:
            script.main()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), "test ok")
