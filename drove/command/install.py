#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
from .generic import Command
from .generic import CommandError

from ..package import Package


class InstallCommand(Command):

    def execute(self):
        plugin_dir = self.config.get("plugin_dir", None)

        if not plugin_dir:
            raise CommandError("'plugin_dir' is not configured")

        if self.args.install_global:
            self.plugin_dir = os.path.expanduser(plugin_dir[-1])
        else:
            self.plugin_dir = os.path.expanduser(plugin_dir[0])

        plugin = self.args.plugin

        if os.path.exists(plugin) and \
           os.path.isfile(plugin):
            if plugin.endswith(".tar.gz"):
                # File exists and it's a tar.gz
                self.log.info("Installing '%s' into '%s'" %
                              (plugin, self.plugin_dir,))

                package = Package(plugin, self.args.verbose)
                package.install(self.plugin_dir)
                sys.exit(0)
