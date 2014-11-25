#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
from . import Command
from . import CommandError

"""This module implements the ``list`` command which can be invoked from
the commandline.

For more help, please run:

.. code-block:: sh

    $ drove list -h

"""


class ListCommand(Command):
    """This class extends :class:`Command` and implement the ``list``
    command used by drove client to list installed plugins.
    """
    def execute(self):
        plugin_dir = self.config.get("plugin_dir", None)
        if not plugin_dir:
            raise CommandError("Missing plugin_dir in configuration")
        for dirname in plugin_dir:
            for author_name in os.listdir(os.path.expanduser(dirname)):
                author_dname = os.path.join(dirname, author_name)
                if author_name[0] != "_" and os.path.isdir(author_dname):
                    for plugin_name in os.listdir(author_dname):
                        plugin_dname = os.path.join(author_dname, plugin_name)
                        if plugin_name[0] != "_" and \
                           os.path.isdir(plugin_dname):
                            self.log.info("%s.%s" % (author_name,
                                                     plugin_name,))
