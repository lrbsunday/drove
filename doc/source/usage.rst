Usage
=====

The main goal of **drove** is to provide a easy way to monitoring and gather
statistics from anuy sources to any destinations. This is too generic, so in
this section we learn how to configure **drove** to act as server or client,
set a number of plugins and running as daemon.

Configure drove core
--------------------

**drove** reads the configuration from a different paths. By default try to
find the configuration in the following paths (in order of precedence):

1. ``$HOME/.config/drove/drove.conf``
2. ``$HOME/.drove/drove.conf``
3. ``/etc/drove.conf``
4. *embeded config in the package*

.. hint::
  You can always override this path using the ``-C`` flag in command line.

The configuration file is basically a WCFG config file, which support the
WCFG grammar (read more about the WCFG grammar in the `wcfg oficial page`_).
You can see that the config syntax is very intuitive and confortable.

There are a number of important variables to explain:

``read_interval`` and ``write_interval``
  Set the number of seconds to wait between two consecutive reads (or
  writes) for the same plugin. This defines basically when drove will go to
  gather info and when dispatch the gathered data to to writters.
  For example:

.. code-block:: yaml

  # we gather values each ten seconds.
  read_interval: 10
  # we dispatch values each minute.
  write_interval: 60


``plugin_dir``
  Set the plugin path (in order of precedence) where drove plugins must be.
  **drove** will try to load plugins from these directories.

.. code-block:: yaml

  plugin_dir: [ "~/.drove/plugins", "/tmp/plugins" ]


``reload``
  Set the number in seconds to wait between two consecutives reloads of the
  configuration.

  **drove** will reload the configuration and plugins each *reload* seconds
  to keep the plugins and config fresh. So if you change the config you
  don't need to restart or reload the daemon.

.. code-block:: yaml

  # reload config each 60 seconds
  reload: 60

``include``
  Include other configuration file. You can use here any glob expression,
  but **only one include is allowed from each config file**.


.. code-block:: yaml

  # include all conf and config files in the same directory that
  # current config file
  include "*.conf*"

.. caution::
  Please remember that you can only set one ``include`` from each file, you
  can use a glob to avoid the problem to load two or more files.

.. _`wcfg oficial page`: https://github.com/aperezdc/python-wcfg

Install plugins
---------------

You can install plugins for drove directly from `Plugins Repository`_ using
the drove client itself, with the command:

.. _`Plugins Repository`: https://plugins.drove.io

.. code-block:: sh

  $ drove install [plugin]

Or you can install a plugin from URL, or from folder:

.. code-block:: sh

  $ drove install http://myurl/plugin.tar.gz

  $ drove install /tmp/myplugindir

.. hint::
  During the installation the plugin can run tests to ensure that the
  plugins is working fine in your system (this usually requires more
  dependencies)

Once the plugin is installed you need to configure it in the drove
configuration file. The usual way to do this is to create a new config file
for the plugin and ``include`` it from main config file.

The config file for a generic plugin looks like this:

.. code-block:: yaml

  plugins.author.plugin {
    variable: value
  }

**drove** use a hierarchical configuration, so each plugin can be declared
as child of ``plugins``. When **drove** starts (or reloads) get the childs
of ``plugins`` and try to load the plugin *author.plugin* from the path,
using the configuration defined inside the block.

The following example configure the plugin |droveio.df|_ (which gather
disk usage from the OS), and it's self explanatory:

.. code-block:: yaml

  plugins.droveio.df {
    include: ["/", "/mnt", "/tmp" ]
  }

In this config, the plugin |droveio.df|_ is configured to get the usage of
the mountpoints ``/``, ``/mnt`` and ``/tmp``.

Running the daemon
------------------

Once you have drove and plugins configurated, it's time to run the daemon.
To run the daemon just run

.. code-block:: sh

  $ drove daemon

And **drove** will start to run in background, detached from the terminal.
This is the normal operation of **drove**, but if you want to run in
foreground for any reason (for example you want to use supervisor_), then
you can run

.. code-block:: sh

  $ drove daemon -f

.. _supervisor: http://supervisord.org/

There are other interesting flags for daemonize drove, please don't hesitate
to read the online help with ``-h`` flag.

And it's all. Now you hace drove up and running.

.. |droveio.df| replace:: ``droveio.df``
.. _droveio.df: https://plugins.drove.io/droveio/df
