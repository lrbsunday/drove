#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
import shutil
import unittest
import drove.script as drove

from drove.package import PackageError
from drove.command.generic import Command
from drove.command.generic import CommandError
from drove.command.search import SearchCommand, urllib


class TestScript(unittest.TestCase):

    def setUp(self):
        self._fork = os.fork
        self._reloader_start = drove.drove.reloader.Reloader.start
        self._pluginmanager_loop = drove.drove.plugin.PluginManager.loop
        self._path = sys.path
        self._from_name = Command.from_name
        self._print_help = drove.argparse.ArgumentParser.print_help
        self._print_item = SearchCommand.print_item
        self._urlopen = urllib.request.urlopen
        self._write = sys.stdout.write

    def tearDown(self):
        sys.argv = ["prog"]
        os.fork = self._fork
        drove.drove.reloader.Reloader.start = self._reloader_start
        drove.drove.plugin.PluginManager.loop = self._pluginmanager_loop
        sys.path = self._path
        Command.from_name = self._from_name
        drove.argparse.ArgumentParser.print_help = self._print_help
        SearchCommand.print_item = self._print_item
        urllib.request.urlopen = self._urlopen
        sys.stdout.write = self._write

    def test_drove_noarg(self):
        """Testing drove: no args"""
        sys.argv = ["prog"]
        drove.argparse.ArgumentParser.print_help = lambda x: None
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 2)

    def test_drove_exit_handler(self):
        """Testing drove: exit_handler"""
        class _plugins(object):
            stop_all = lambda *a, **kw: None

        class _log(object):
            error = lambda *a, **k: None
            info = error
            warning = error

        class _mock(object):
            def __init__(self):
                self.log = _log()
                self.plugins = _plugins()

        import drove.command.daemon as daemon
        f = daemon.DaemonCommand._exit_handler
        obj = _mock()
        with self.assertRaises(SystemExit) as cm:
            f(obj)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 15)

    def _mock_from_name(self, *args, **kw):
        raise AssertionError("Mocked exception")

    def test_drove_main_except(self):
        """Testing drove: main catch exception"""
        sys.argv = ["prog", "daemon", "-f", "-np"]
        Command.from_name = self._mock_from_name
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 128)

    def test_drove_flags(self):
        """Testing drove: main flags"""
        sys.argv = ["prog", "-v", "daemon", "-np", "-f"]
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_drove_config(self):
        """Testing drove: -C flag"""
        config_file = os.path.join(os.path.dirname(__file__),
                                   "config", "empty.conf")
        sys.argv = ["prog", "-C", config_file, "daemon", "-np", "-f"]
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_drove_config_default(self):
        """Testing drove: default config"""
        sys.argv = ["prog", "daemon", "-np", "-f"]
        config = drove.DEFAULT_CONFIG_FILES
        config_file = os.path.join(os.path.dirname(__file__),
                                   "config", "empty.conf")
        drove.DEFAULT_CONFIG_FILES = [config_file]
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        drove.DEFAULT_CONFIG_FILES = config
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_drove_environment_ok(self):
        """Testing drove: -s flag with fine parameters"""
        sys.argv = ["prog", "-s", "key=value", "daemon", "-np", "-f"]
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_drove_environment_fail(self):
        """Testing drove: -s flag with fine parameters"""
        sys.argv = ["prog", "-s", "key", "daemon", "-np", "-f"]
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 2)

    def test_drove_daemon(self):
        """Testing drove: daemon"""
        sys.argv = ["prog", "daemon"]
        os.fork = lambda: 0
        drove.drove.reloader.Reloader.start = lambda x: None
        drove.drove.plugin.PluginManager.loop = lambda x: None
        drove.main()

    def test_drove_daemon_foreground(self):
        """Testing drove: daemon (-f)"""
        sys.argv = ["prog", "daemon", "-f"]
        os.fork = lambda: 0
        drove.drove.reloader.Reloader.start = lambda x: None
        drove.drove.plugin.PluginManager.loop = lambda x: None
        drove.main()

    def test_drove_daemon_interrupt(self):
        """Testing drove: daemon with KeyboardInterrupt"""
        sys.argv = ["prog", "daemon"]
        os.fork = lambda: 0

        def _interrupt(x):
            raise KeyboardInterrupt()

        drove.drove.reloader.Reloader.start = lambda x: None
        drove.drove.plugin.PluginManager.loop = _interrupt
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 15)

    def test_drove_daemon_exception(self):
        """Testing drove: daemon with BaseException"""
        sys.argv = ["prog", "daemon"]
        os.fork = lambda: 0

        def _interrupt(x):
            raise Exception()

        drove.drove.reloader.Reloader.start = lambda x: None
        drove.drove.plugin.PluginManager.loop = _interrupt
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)

    def test_drove_daemon_exception_verbose(self):
        """Testing drove: daemon with BaseException (-v)"""
        sys.argv = ["prog", "-v", "daemon"]
        os.fork = lambda: 0

        def _interrupt(x):
            raise Exception()

        drove.drove.reloader.Reloader.start = lambda x: None
        drove.drove.plugin.PluginManager.loop = _interrupt
        with self.assertRaises(Exception):
            drove.main()

    def test_drove_setproctitle(self):
        """Testing drove: setproctitle"""
        sys.argv = ["prog", "-v", "daemon", "-np", "-f"]
        sys.path.insert(0, os.path.dirname(__file__))
        with self.assertRaises(ValueError) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), "test ok")

    def test_drove_list(self):
        """Testing drove: listing installed packages"""
        here = os.path.join(os.path.dirname(__file__), "installed_plugins")
        sys.argv = ["prog", "-P", here, "list"]
        drove.main()
        sys.argv = ["prog", "-v", "-s", "plugin_dir=", "list"]
        with self.assertRaises(CommandError):
            drove.main()

    def test_drove_install_tarball(self, using_global=False,
                                   dest="installed_plugins",
                                   tarball="test2-okay-1.0.tar.gz",
                                   exit_code=0):
        """Testing drove: install tarball"""
        here = os.path.join(os.path.dirname(__file__), dest)
        plug = os.path.join(os.path.dirname(__file__), tarball)
        sys.argv = ["prog", "-P", here, "install"]
        if using_global:
            sys.argv.append("--global")
        sys.argv.append(plug)
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, exit_code)

        if using_global:
            # reinstall and failed
            with self.assertRaises(PackageError):
                sys.argv = ["prog", "-v", "-P", here, "install", plug]
                drove.main()

        sys.argv = ["prog", "-P", here, "remove", "test2.okay"]
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

    def test_drove_install_tarball_global(self):
        """Testing drove: install tarball (--global)"""
        self.test_drove_install_tarball(using_global=True)

    def test_drove_install_tarball_nopip(self):
        """Testing drove: install tarbal (no pip installed)"""
        # XXX probably pip is already loaded
        if "pip" in sys.modules:
            del sys.modules["pip"]
        sys.path = [os.path.join(os.path.dirname(__file__), "fakemods")]
        import pip
        assert hasattr(pip, "mocked")
        self.test_drove_install_tarball(exit_code=128)

    def test_drove_install_tarball_nodir(self):
        """Testing drove: install tarball (no dir)"""
        here = os.path.join(os.path.dirname(__file__), "notinstalled_dir")
        plug = os.path.join(os.path.dirname(__file__), "test2-okay-1.0.tar.gz")
        sys.argv = ["prog", "-v", "-P", here, "install", plug]
        with self.assertRaises(PackageError):
            drove.main()

    def test_drove_install_command_error(self):
        """Testing drove: install (command error)"""
        here = os.path.join(os.path.dirname(__file__), "installed_plugins")
        plug = os.path.join(os.path.dirname(__file__), "test2-bad-1.0.tar.gz")
        sys.argv = ["prog", "-v", "-s", "plugin_dir=", "install", plug]
        with self.assertRaises(CommandError):
            drove.main()

        sys.argv = ["prog", "-v", "-s", "plugin_dir=", "remove", "test2.bad"]
        with self.assertRaises(CommandError):
            drove.main()

        sys.argv = ["prog", "-v", "-P", here, "remove", "test"]
        with self.assertRaises(CommandError):
            drove.main()

    def test_drove_remove_empty(self):
        """Testing drove: remove empty folder"""
        here = os.path.join(os.path.dirname(__file__), "installed_plugins")
        sys.argv = ["prog", "-v", "-P", here, "remove", "other.test"]
        with self.assertRaises(SystemExit) as cm:
            drove.main()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)
        shutil.copytree(os.path.join(here, "_base"),
                        os.path.join(here, "other"))

    def test_drove_install_tarball_error(self):
        here = os.path.join(os.path.dirname(__file__), "installed_plugins")
        with self.assertRaises(PackageError):
            plug = os.path.join(os.path.dirname(__file__),
                                "test2-empty-1.0.tar.gz")
            sys.argv = ["prog", "-v", "-P", here, "install", plug]
            drove.main()

        with self.assertRaises(PackageError):
            plug = os.path.join(os.path.dirname(__file__),
                                "test2-none-1.0.tar.gz")
            sys.argv = ["prog", "-v", "-P", here, "install", plug]
            drove.main()

    def test_drove_search(self):
        """Testing drove: search"""
        class _mock(object):
            def read(self):
                return bytes('{"results": [{"version": ' +
                             '[{"download_url": "...", ' +
                             '"id": "1.0"}], "description":' +
                             '"test", "id": "test/test"}]}',
                             'utf-8')

            def close(self):
                pass

        sys.argv = ["prog", "search", "example"]
        urllib.request.urlopen = lambda x: _mock()
        drove.main()

    def test_drove_malformed(self):
        """Testing drove: search (malformed)"""
        class _mock(object):
            def read(self):
                return bytes('{}', 'utf-8')

            def close(self):
                pass

        sys.argv = ["prog", "-v", "search", "example"]
        urllib.request.urlopen = lambda x: _mock()
        with self.assertRaises(CommandError):
            drove.main()

    def test_drove_search_none_found(self):
        """Testing drove: search (none found)"""
        class _mock(object):
            def read(self):
                return bytes('{"results": []}', 'utf-8')

            def close(self):
                pass

        sys.argv = ["prog", "search", "example"]
        urllib.request.urlopen = lambda x: _mock()
        drove.main()


