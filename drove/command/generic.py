#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""The generic command module provides a generic way to load
specific drove client commands.
"""

from ..importer import Importer


class CommandError(Exception):
    """Models an error running a client command"""


class Command(object):
    def __init__(self, config, args, log):
        self.config = config
        self.args = args
        self.log = log

    @classmethod
    def from_name(cls, name, config, args, log):
        kls = Importer("drove.command", class_suffix="Command")
        return kls(name, config, args, log)
