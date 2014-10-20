#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import socket
import unittest
import drove.util.network


def _mocked_getaddrinfo(*args, **kwargs):
    return None


class TestUtilNetwork(unittest.TestCase):

    def test_parse_addr(self):
        """Testing util.network: parse_addr() basic behaviour"""
        assert drove.util.network.parse_addr("127.0.0.1:12", resolve=False) == \
            ("127.0.0.1", 12, socket.AF_INET)

        assert drove.util.network.parse_addr("127.0.0.1", defport=12) == \
            ("127.0.0.1", 12, socket.AF_INET)

        assert drove.util.network.parse_addr("[::1]:12") == \
            ("::1", 12, socket.AF_INET6)

        assert drove.util.network.parse_addr("[::1]", defport=12) == \
            ("::1", 12, socket.AF_INET6)

        assert drove.util.network.parse_addr("localhost:12") in [
            ("::1", 12, socket.AF_INET6), ("127.0.0.1", 12, socket.AF_INET)]

    def test_parse_addr_empty(self):
        """Testing util.network: parse_addr() empty address"""
        with self.assertRaises(ValueError):
            drove.util.network.parse_addr("")

    def test_parse_addr_fail(self):
        """Testing util.network: parse_addr() bad address"""
        with self.assertRaises(ValueError):
            drove.util.network.parse_addr("300.0.0.1:12")

    def test_parse_addr_fail_resolve(self):
        """Testing util.network: parse_addr() cannot resolve"""
        with self.assertRaises(ValueError):
            drove.util.network.socket.getaddrinfo = _mocked_getaddrinfo
            drove.util.network.parse_addr("127.0.0.1:12")

    def test_getfqdn(self):
        """Testing util.network: getfqdn()"""
        x = drove.util.network.getfqdn
        x.reload()
        assert isinstance(str(x), str)
