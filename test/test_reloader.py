#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import drove.reloader


class MockObject(object):
    def reload(self):
        pass


def test_timer():
    """Testing Reloader: basic behaviour"""
    x = drove.reloader.Reloader([MockObject()])
    x.reload()
