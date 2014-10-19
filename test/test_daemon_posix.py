#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
from nose.tools import raises
from nose.tools import with_setup
from drove.daemon import Daemon

if os.name == "posix":

    _fork = os.fork

    def test_daemon_posix():
        """Testing daemon.posix: basic behaviour"""
        d = Daemon.create(lambda: None, lambda: None)
        d.foreground()
        os.fork = lambda: 0
        d.start()
        d.restart()
        os.fork = _fork


