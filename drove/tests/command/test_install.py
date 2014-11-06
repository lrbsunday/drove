#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import unittest

from drove.util import temp
from drove.config import Config
from drove.util.log import getLogger
from drove.command import CommandError
from drove.command.install import InstallCommand


class TestInstallCommand(unittest.TestCase):
    name = "test.install"

    class _mock_str(str):
        pass

    def test_install_command(self, install_global=False, plugin=__file__):
        self.plugin = TestInstallCommand._mock_str(plugin)
        self.plugin.endswith = lambda x: True
        self.install_global = install_global
        self.upgrade = True

        config = Config()
        config["plugin_dir"] = ["none"]

        with temp.variables({
            "drove.package.Package.from_tarball": lambda *a, **kw: self
        }):
            cmd = InstallCommand(config, self, getLogger())
            assert cmd.__class__.__name__ == "InstallCommand"
            cmd.execute()

    def test_install_command_global(self):
        self.test_install_command(True)

    def test_install_command_invalidurl(self):
        with self.assertRaises(CommandError):
            self.test_install_command(False, "invalid://none")

    def test_install_noplugindir(self):
        config = Config()
        self.plugin = "none"
        self.install_global = False
        self.upgrade = False

        with self.assertRaises(CommandError):
            cmd = InstallCommand(config, self, getLogger())
            cmd.execute()

    def test_install_filenotarball(self):
        config = Config()
        config["plugin_dir"] = os.path.dirname(__file__)
        self.plugin = __file__
        self.install_global = False
        self.upgrade = False

        with self.assertRaises(CommandError):
            cmd = InstallCommand(config, self, getLogger())
            cmd.execute()

    def test_install_fromurl(self):
        self.plugin = "http://none"
        self.install_global = False
        self.upgrade = False

        config = Config()
        config["plugin_dir"] = ["none"]

        with temp.variables({
            "drove.package.Package.from_url": lambda *a, **kw: self
        }):
            cmd = InstallCommand(config, self, getLogger())
            assert cmd.__class__.__name__ == "InstallCommand"
            cmd.execute()
