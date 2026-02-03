===============
Useful Commands
===============


Pygame Installation
===================

If you have problems installing the pygame package, try running the following command:

.. code-block:: console

    pip install pygame --pre


Generate, Run, Visualize
========================

As you're testing your code, it's important to do these three actions.

* **Generate** a new map and seed.
* **Run** a game using your client and generated map.
* **Visualize** what happened in the last ran game.

To do so, use the provided "launcher":

.. code-block::

   python launcher.pyz <command>

where ``<command>`` describes the action you want to perform:

.. csv-table::
   :header: "Action", "<command>"

    "Generate", "g, gen, generate"
    "Run", "r, run"
    "Visualize", "v, vis, visualize"

You can also combine certain commands:

.. code-block:: console
   :caption: Do everything

   python launcher.pyz grv

.. code-block::
   :caption: Generate and run, but don't visualize

    python launcher.pyz gr

Generate
--------

If you don't want to have a new, random seed, don't run this command. With the same seed and clients, the results will
stay consistent.


Run
---

As the game is running, any print statements you have will print to your console, which can be useful for
debugging. There will also be logs generated in the ``logs`` folder, showing what information was stored each turn in
the JSON format.

Visualize
---------

This displays each turn of the game you ran, allowing you to debug in a more user-friendly way! How wonderful.
Visit :doc:`visualizer` to get a better understanding of how it works.

Launcher Help
-------------

To see every possible command combination, run

.. code-block::

    python launcher.pyz -h

Some commands have their own help messages, which can be displayed via

.. code-block::

   python launcher.pyz <command> -h
