#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""The generic command module provides a generic way to load
specific drove client commands.
"""

from ..util import importer


class CommandError(Exception):
    """Models an error running a client command"""


class Command(object):
    def __init__(self, config, args, log):
        self.config = config
        self.args = args
        self.log = log

    @classmethod
    def from_name(cls, name, config, args, log):
        mod_name = ".%s" % (name,)
        kls_name = "%sCommand" % (name.title(),)

        kls = importer.load(mod_name, kls_name, anchor=__package__)
        return kls(config, args, log)
