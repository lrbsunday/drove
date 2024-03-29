Plugins
=======

The plugins are the secret sauce of **drove**. Due to drove design, the core
daemon only handles reader and writer plugins. That means that all logic in
the collection process belongs to specific plugins. Plugins can be readers
(for example ``droveio.cpu``), writers (for example ``droveio.influxdb``)
or both (for example ``droveio.network``).

Installing plugins
------------------

To install plugin you can use the drove client, just typing:

.. code-block:: bash

  $ drove install [plugin]

Where plugin could be one of the following values:

1. A plugin name. Then drove will connect to the repository to resolve the
   name and get the proper code. You can set the URL of the repository
   setting the variable ``plugin_repo`` in the main config file. By default
   uses the public plugin repository from https://plugins.drove.io

2. A path to a ``tar.gz`` file which contain the plugin in the proper format
   (read `How to pack a plugin`_ for more information)

3. An URL to get the package from. The package must be well formated.

Create new plugin
-----------------

The drove plugins are python modules with a specific packaging. To create
new plugin you need to create first a python module with your plugin.

For example for plugin ``droveio.cpu`` we created the file ``cpu.py`` inside
folder ``droveio`` (``droveio`` is the author of the plugin).

Inside this file you must have a class with the same name as the module, but
in camel case notation and ``Plugin`` suffix. For our cpu example, must be
something like this:

.. code-block:: python

  from drove.plugin import Plugin

  class CpuPlugin(Plugin):
    # Example of plugin

Note that the class must extend from :class:`drove.plugin.Plugin`.

Finally, you need to create some code for your plugin. Basically you want to
implement any of the following three functions:

``def setup(self)``
  This function will called from drove when the plugin is loaded and only
  once. Tipically you can use this function to set some generic values, read
  some configuration or initialize things which needs to be available where
  the plugin lives.

``def read(self)``
  This function will run periodically each ``read_interval`` seconds, as
  defined in configuration file (read :doc:`usage` for more information).
  In this function you can call to :meth:`drove.plugin.Plugin.emit` to send
  values or events to core.

``def write(self, channel)``
  This function will receive a :class:`drove.channel.Channel` object to get
  cached values get from ``read`` function above. This function is the
  responsible to unqueue data from channel and do something with them
  (usually persist that values in some way)


There is an example, which generate random values and write them in
``stdout``:

.. code-block:: python

  import random
  from drove.plugin import Plugin
  from drove.data.value import Value

  class RandomPlugin(Plugin):
    def setup(self):
      self.log.info("initializing random plugin")

    def read(self):
      self.emit(Value("random", random.randint(0, 10)))

    def write(self, channel):
      for data in channel.receive("random"):
        print(data)


How to pack a plugin
--------------------

Plugins must be packed in a proper format to be understandable for
**drove**. Basically you must follow the next specification for the
directories::

  root dir
  ├── README.rst               [optional]
  ├── config                   [optional]
  │   └── plugin_name.conf     [optional]
  ├── plugin                   [mandatory]
  │    └── author              [mandatory]
  │        ├── __init__.py     [mandatory]
  │        └── plugin_name.py  [mandatory]
  ├── requirements.txt         [optional]
  └── tests                    [optional]
      └── test_plugin_cpu.py   [optional]


Inside the ``plugin`` directory you **MUST** have a directory with the name
of the author, which include the module. Please note that you can use
a package instead a module if your module contains a lot of files::

  plugin
  └── author
      ├── plugin
      │   ├── mycode.py
      │   └── __init__.py
      └── __init__.py

Please note that you can only add one plugin per package (module or package,
but just one).

The author in package is just a string, has no special meaning, and is only
use to create a properly namespace.

For example, for the ``droveio.cpu`` plugin, this is the directory tree::

  droveio-cpu-1.0
  ├── README.rst
  ├── config
  │   └── cpu.conf
  ├── plugin
  │   └── droveio
  │       ├── __init__.py
  │       └── cpu.py
  ├── requirements.txt
  └── tests
      └── test_plugin_cpu.py

If ``test/`` directory exists, then drove will test the plugin before
install it, which is highly recommended.
