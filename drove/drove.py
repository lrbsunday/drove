#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""This module contains command line endpoints to run the program from shell
"""

import os
import sys
import argparse

import drove
import drove.log
import drove.daemon
import drove.config
import drove.plugin
import drove.channel
import drove.reloader

from drove.util.network import getfqdn


DEFAULT_CONFIG_FILES = ["~/.config/drove/drove.conf",
                        "~/.drove/drove.conf",
                        "/etc/drove/drove.conf",
                        os.path.join(os.path.dirname(__file__), "config",
                                     "drove.conf")]


def _daemon(config, plugins, log, args):
    try:
        plugins.start_all()

        # starting reload thread
        log.debug("Starting reloader")
        reloader = drove.reloader.Reloader([getfqdn, config] +
                                           [x for x in plugins],
                                           interval=config.get(
                                               "reload",
                                               60))
        reloader.start()

        # wait until all plugins stop
        log.info("Entering data gathering loop")
        plugins.loop()

    except KeyboardInterrupt:
        log.fatal("Received a Keyboard Interrupt. Exit silently.")
        sys.exit(15)
    except BaseException as e:
        if args.verbose:
            raise
        log.fatal("Unexpected error happened during drove execution: " +
                  "{message}".format(message=str(e)))
        sys.exit(1)


def _exit_handler(log, plugins):
    if log:
        log.error("Received TERM signal. Try to exit gently...")
    if plugins:
        plugins.stop_all()
    sys.exit(15)


def main():
    """Base command line executable.
    """

    cmdopt = argparse.ArgumentParser(
        description="%s %s: %s" % (drove.NAME, drove.VERSION,
                                   drove.DESCRIPTION,))

    cmdopt.add_argument("-C", "--config-file", action="store",
                        dest="config_file",
                        help="Main configuration file to read.",
                        type=str,
                        default=None)

    cmdopt.add_argument("-v", "--verbose", action="store_true",
                        dest="verbose",
                        help="be verbose",
                        default=False)

    cmdopt.add_argument("-s", "--set", action="append",
                        dest="set",
                        help="set config variables by hand (key=value). " +
                             "This option will override values from " +
                             "config file.",
                        default=[])

    cmdopt.add_argument('-V', '--version', action='version',
                        version="%(prog)s " + drove.VERSION)

    cmdopt.add_argument('-np', '--exit-if-no-plugins', action='store_true',
                        dest="exit_if_no_plugins",
                        help="if true drove exists if no plugins found",
                        default=False)

    cmdopt.add_argument('-f', '--foreground', action='store_true',
                        dest="foreground",
                        help="No daemonize and run in foreground.",
                        default=False)

    args = cmdopt.parse_args()
    log = drove.log.getDefaultLogger()

    # read configuration and start reload timer.
    if args.config_file:
        config = drove.config.Config(args.config_file)
    else:
        config = drove.config.Config()
        for cf in DEFAULT_CONFIG_FILES:
            cf = os.path.expanduser(cf)
            if os.path.isfile(cf):
                config = drove.config.Config(cf)

    if args.set:
        for config_val in args.set:
            if "=" not in config_val:
                log.error("--set option require a 'key=value' value.")
                sys.exit(2)
            key, val = config_val.split("=", 1)
            config[key] = val

    # ensure that config has nodename or create nodename for this node
    if config.get("nodename", None) is None:
        config["nodename"] = getfqdn

    # configure log, which is a singleton, no need to use parameters
    # in log in any other places.
    log = drove.log.getLogger(syslog=config.get("syslog", True),
                              console=config.get("logconsole", False),
                              logfile=config.get("logfile", None),
                              logfile_size=config.get("logfile_size", 0),
                              logfile_keep=config.get("logfile_keep", 0))
    if args.verbose:
        log.setLevel(drove.log.DEBUG)

    try:
        from setproctitle import setproctitle
        setproctitle("drove %s" % " ".join(sys.argv[1:]))
    except ImportError:
        pass

    log.info("Starting drove")

    # create a common channel to communicate the plugins
    log.debug("Creating channel")
    channel = drove.channel.Channel()

    # starting plugins
    log.debug("Starting plugins")
    plugins = drove.plugin.PluginManager(config, channel)

    if len(plugins) == 0:
        log.warning("No plugins installed... " +
                    "drove has no work to do.")
        if args.exit_if_no_plugins:
            sys.exit(0)

    # setup daemon, but not necessary run in background
    daemon = drove.daemon.Daemon.create(
        lambda: _daemon(config, plugins, log, args),
        lambda x: _exit_handler(plugins, log))
    if args.foreground:
        # starting daemon in foreground if flag is preset
        daemon.foreground()
    else:
        # or start it as daemon
        return daemon.start()