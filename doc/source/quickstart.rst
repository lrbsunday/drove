Quickstart
==========

This is a 10 minute guide to install drove with minimal plugin configuration
to monitoring a simple host.

First of all be sure that you have almost python >= 2.7.0 installed on your
system. Then install pip and distribute (usually all this dependencies are
installed by default in your operating system).

Finally, install drove:

.. code-block:: sh

  $ sudo pip install drove

Once you have drove installed, is time to run it and test that everything
works fine:

.. code-block:: sh

  $ drove -v -s logconsole=true daemon -np -f
  [2014-11-17 15:18:29,916]   INFO       Starting drove daemon (0.2)
  [2014-11-17 15:18:29,917]   INFO       Using configuration file: /drove/config/drove.conf
  [2014-11-17 15:18:29,917]   DEBUG      Creating channel
  [2014-11-17 15:18:29,917]   DEBUG      Starting plugins
  [2014-11-17 15:18:29,917]   WARNING    No plugins installed... drove has no work to do.
  $

We just run drove daemon with some options, concretly ``-v`` which means *be
verbose*, ``-s logconsole=true`` which forces drove to log output in stderr,
``-np`` which means *no plugins* and provokes that if there are no
configured plugins, the daemon dies and ``-f`` which means *foreground*,
which avoid drove to go to background.

Now is time to instal any plugin. For example a basic CPU collector:

.. code-block:: sh

  $ drove install droveio.cpu

That install the oficial *droveio* plugin for *cpu*.

Now we need to activate the plugin, editing ``/etc/drove.conf``, and adding
the following lines to enable the plugin::

  plugin.droveio.cpu: true

Then you can start your daemon in background

.. code-block:: sh

  $ drove daemon

Ok, now we have a drove daemon collecting CPU data, which is cool, but we
need to do something with this data.

.. note :: If you do not understand how drove works, please read :doc:`index` section
  before continue.

We can use in this example the influxdb plugin. Influxdb_ is a time series
database which fits well for drove mechanics. You need to install influxdb
before continue. Please read the installation_ section in influx
documentation.

.. _installation: http://influxdb.com/docs/v0.8/introduction/installation.html
.. _Influxdb: http://influxdb.com

After install Influxdb, we need to install the influxdb drove plugin:

.. code-block:: sh

  $ drove install droveio.influxdb

And configure the plugin in ``/etc/drove.conf``::

  plugin.droveio.influxdb {
   host: "127.0.0.1"
   port: "8086"
   database: "drove"
   user: "admin"
   password: "admin"
  }

Then restart the drove daemon:

.. code-block:: sh

  $ pkill *drove*
  $ drove daemon

Your drove installation is ready. Now you have a drove daemon acting as
agent, collecting data from CPU using *droveio.cpu* plugin, and writing data
in influxdb, using *droveio.influxdb* plugin.

