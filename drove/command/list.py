#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import glob
from .generic import Command
from .generic import CommandError


class ListCommand(Command):
    def execute(self):
        plugin_dir = self.config.get("plugin_dir", None)
        if not plugin_dir:
            raise CommandError("Missing plugin_dir in configuration")
        for dirname in plugin_dir:
            for author_name in glob.glob(os.path.join(
                os.path.expanduser(dirname), "*")
            ):
                author_sname = os.path.basename(author_name)
                if author_sname[0] != "_" and os.path.isdir(author_name):
                    for plugin_name in glob.glob(
                        os.path.join(author_name, "*")
                    ):
                        plugin_sname = os.path.basename(plugin_name)
                        if plugin_sname[0] != "_" and \
                           os.path.isdir(plugin_name):
                            self.log.info("%s.%s" % (author_sname,
                                                     plugin_sname,))
