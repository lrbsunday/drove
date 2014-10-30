#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
import shutil
from .generic import Command
from .generic import CommandError


class RemoveCommand(Command):
    def execute(self):
        plugin_dir = self.config.get("plugin_dir", None)
        if not plugin_dir:
            raise CommandError("Missing plugin_dir in configuration")

        if "." not in self.args.plugin:
            raise CommandError("plugin must contain almost author.plugin")

        author, plugin = self.args.plugin.split(".", 1)

        for directory in plugin_dir:
            directory = os.path.expanduser(directory)

            candidate = os.path.join(directory, author, plugin)
            if os.path.isdir(candidate):
                self.log.info("Removing plugin '%s.%s'" %
                              (author, plugin,))
                shutil.rmtree(candidate, ignore_errors=True)

            author_dir = os.path.join(directory, author)

            if os.path.isdir(author_dir) and \
               not [x for x in os.listdir(author_dir) if x[0] != "_"]:
                self.log.info("Removing empty author folder '%s'" %
                              (author,))
                shutil.rmtree(author_dir)
        sys.exit(0)
