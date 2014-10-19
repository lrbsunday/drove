#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
from drove.daemon import Daemon
from nose.tools import with_setup

if os.name == "posix":

    _fork = os.fork
    _kill = os.kill

    def _tear_down():
        os.fork = _fork
        os.kill = _kill

    @with_setup(teardown=_tear_down)
    def test_daemon_posix():
        """Testing daemon.posix: parent behaviour"""
        d = Daemon.create(lambda: None, lambda: None)
        d.foreground()
        os.fork = lambda: 0
        d.start()
        d.restart()
        os.fork = _fork

    @with_setup(teardown=_tear_down)
    def test_daemon_posix_child():
        """Testing daemon.posix: child behaviour"""
        d = Daemon.create(lambda: None, lambda: None)
        os.fork = lambda: 100
        os.kill = lambda x, y: None
        d.start()
        assert d.pid == 100
        d.stop()
