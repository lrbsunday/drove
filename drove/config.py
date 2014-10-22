#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""This module contains classes to parse configuration files and
create python dictionary based class to handle it.
"""

import os
import wcfg
import glob


class ConfigError(Exception):
    """Models an exception reading config."""


CONFIG_UNSET = (None,)


class Config(dict):
    """Parse a config file and create an object to get the paramters,
    with the ability to reload the config online.

    :param config_file: the main configuration file to load.
        If not set you need to populate the config using the
        :meth:`reload`
    """
    def __init__(self, config_file=None):
        self.config_file = config_file
        self.config_mtime = 0

        if config_file is not None:
            self.reload()

    def reload(self, config_file=None):
        """Reload the config.

        :param config_file: if set populate config from this config
            file. If not use the config defined in constructor.
        """
        config_file = config_file or self.config_file
        with open(config_file, 'rb') as f:
            contents = wcfg.load(f)

        self.update(contents)

        if "include" in contents:
            if contents["include"][0] != '/':
                include = os.path.join(
                    os.path.dirname(config_file), contents["include"]
                )
            else:
                include = contents["include"]
            for f in glob.glob(include):
                self.reload(f)

    def get(self, key, default=CONFIG_UNSET):
        """Return a value for a key in the config. If
        this key is not found and no default value is
        provided, raises a :class:`ConfigError` exception.
        If default value is provided and key not found,
        the default value is returned.

        :param key: the key to search in config
        :param default: the default value to return
            in case that key not found in config.
        """
        if key in self:
            return dict.get(self, key)
        elif "." in key:
            try:
                parent, _, key = key.rsplit(".", 2)
                return self.get(parent + "." + key, default)
            except ValueError:
                parent, key = key.split(".", 1)
                return self.get(key, default)
        elif default != CONFIG_UNSET:
            return default
        else:
            raise ConfigError("Required config parameter " +
                              "'%s' not found" % (key,))

    def get_childs(self, prefix):
        """Get the keys which hirarchically depends of prefix
        passed by argument.

        For example:

        >>> x = Config()
        >>> x["namespace.key"] = 1
        >>> x.get_childs("namespace") == ['namespace']

        :type prefix: str
        :param prefix: a string to search keys under that prefix.
        """
        prefix = prefix if prefix[-1] == "." else (prefix + ".")
        childs = set()
        for key in self:
            if key.startswith(prefix):
                suffix = key.replace(prefix, "")
                if "." in suffix:
                    childs.add(suffix.split(".")[0])
                else:
                    childs.add(suffix)
        return childs

    def __getitem__(self, key):
        return self.get(key)
