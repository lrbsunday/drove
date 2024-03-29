#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""This module contains utilities for manage some
networking concepts.

Attributes:
    getfqdn (function): A singleton function which return the current node
    FQDN.
"""

import re
import socket


# The parse_addr function is gently taken from pyptlib project. Credits from
# them.
# https://gitweb.torproject.org/pluggable-transports/pyptlib.git/tree/HEAD

def parse_addr(spec, defhost=None, defport=None, resolve=True):
    """
    Parse a host:port specification and return a 2-tuple ("host", port) as
    understood by the Python socket functions.

    If resolve is true, then the host in the specification or the defhost
    may be a domain name, which will be resolved. If resolve is false, then
    the host must be a numeric IPv4 or IPv6 address.

    IPv6 addresses must be enclosed in square brackets.

    :returns: tuple -- (address, port)

    :raises: ValueError if spec is not well formed.

    >>> parse_addr_spec("192.168.0.1:9999")
    ('192.168.0.1', 9999)

    If defhost or defport are given, those parts of the specification may be
    omitted; if so, they will be filled in with defaults.
    >>> parse_addr_spec("192.168.0.2:8888", defhost="192.168.0.1",
    ...                 defport=9999)
    ('192.168.0.2', 8888)
    >>> parse_addr_spec(":8888", defhost="192.168.0.1", defport=9999)
    ('192.168.0.1', 8888)
    >>> parse_addr_spec("192.168.0.2", defhost="192.168.0.1", defport=9999)
    ('192.168.0.2', 9999)
    >>> parse_addr_spec("192.168.0.2:", defhost="192.168.0.1", defport=9999)
    ('192.168.0.2', 9999)
    >>> parse_addr_spec(":", defhost="192.168.0.1", defport=9999)
    ('192.168.0.1', 9999)
    >>> parse_addr_spec("", defhost="192.168.0.1", defport=9999)
    ('192.168.0.1', 9999)
    """
    host = None
    port = None
    af = 0
    m = None
    # IPv6 syntax.
    if not m:
        m = re.match('^\[(.+)\]:(\d*)$', spec)
        if m:
            host, port = m.groups()
            af = socket.AF_INET6
    if not m:
        m = re.match('^\[(.+)\]$', spec)
        if m:
            host, = m.groups()
            af = socket.AF_INET6
    # IPv4/hostname/port-only syntax.
    if not m:
        try:
            host, port = spec.split(":", 1)
        except ValueError:
            host = spec
        if re.match('^[\d.]+$', host):
            af = socket.AF_INET
        else:
            af = 0
    host = host or defhost
    port = port or defport
    if host is None or port is None:
        raise ValueError("Bad address specification \"%s\"" % spec)

    # Now we have split around the colon and have a guess at the address
    # family.
    # Forward-resolve the name into an addrinfo struct. Real DNS resolution is
    # done only if resolve is true; otherwise the address must be numeric.
    if resolve:
        flags = 0
    else:
        flags = socket.AI_NUMERICHOST
    try:
        addrs = socket.getaddrinfo(host, port, af, socket.SOCK_STREAM,
                                   socket.IPPROTO_TCP, flags)
    except socket.gaierror as e:
        raise ValueError("Bad host or port: \"%s\" \"%s\": %s" % (host, port,
                                                                  str(e)))
    if not addrs:
        raise ValueError("Bad host or port: \"%s\" \"%s\"" % (host, port))

    # Convert the result of socket.getaddrinfo (which is a 2-tuple for IPv4 and
    # a 4-tuple for IPv6) into a (host, port) 2-tuple.
    host, port = socket.getnameinfo(addrs[0][4], socket.NI_NUMERICHOST |
                                    socket.NI_NUMERICSERV)
    port = int(port)
    return host, port, (af or addrs[0][0])


class NodenameFactory(object):
    def __init__(self):
        """A helper class to get current FQDN in cached way,
        but which allows reload method.

        Please do not use this class directly. Instead use
        the module attribute ``getfqdn``
        """
        self.reload()

    def __call__(self):
        return self.nodename

    def __str__(self):
        return self.nodename

    def reload(self):
        """Reload the cached FQDN for this node"""
        self.nodename = socket.getfqdn()

getfqdn = NodenameFactory()
