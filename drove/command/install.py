#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
from six.moves import urllib
from .generic import Command
from .generic import CommandError

from ..package import Package
from ..util import temp


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

        if plugin.startswith("https://") or \
           plugin.startswith("http://"):
            with temp.directory() as tmp_dir:
                tmp_file = os.path.join(tmp_dir, "plugin.tar.gz")
                with urllib.request.urlopen(plugin) as response:
                    with open(tmp_file, 'wb') as out_file:
                        data = response.read()
                        out_file.write(data)

                package = Package(tmp_file, self.args.verbose)
                package.install(self.plugin_dir)
            sys.exit(0)

        if os.path.exists(plugin) and \
           os.path.isfile(plugin):
            if plugin.endswith(".tar.gz"):
                # File exists and it's a tar.gz
                self.log.info("Installing '%s' into '%s'" %
                              (plugin, self.plugin_dir,))

                package = Package(plugin, self.args.verbose)
                package.install(self.plugin_dir)
                sys.exit(0)
