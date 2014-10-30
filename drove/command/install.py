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

        if os.path.exists(self.args.plugin) and \
           os.path.isfile(self.args.plugin):
            if self.args.plugin.endswith(".tar.gz"):
                # File exists and it's a tar.gz
                self.log.info("Installing '%s' into '%s'" %
                              (self.args.plugin, self.plugin_dir,))

                package = Package(self.args.plugin, self.args.verbose)
                package.install(self.plugin_dir)
                sys.exit(0)
