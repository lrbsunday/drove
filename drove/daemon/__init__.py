#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""The data module contains definitions of data used in drove
client-server communication
"""

import os
from ..util import importer


class Daemon(object):
    @classmethod
    def create(cls, handler, exit_handler=None):
        if os.name == "posix":
            mod_name = ".%s" % (os.name,)
            kls_name = "%sDaemon" % (os.name.title())

            kls = importer.load(mod_name, kls_name, anchor=__package__)
            return kls(handler, exit_handler)
        else:
            raise NotImplementedError("The platform '%s' " % (os.name,) +
                                      "is not supported yet. Please drop us " +
                                      "a line if you are interesting in " +
                                      "porting drove to this platform.")
