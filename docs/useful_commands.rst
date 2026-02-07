===============
Useful Commands
===============


Pygame Installation
===================

If you have problems installing the pygame package, try running the following command:

.. code-block:: console

    pip install pygame --pre


.. _enum-script:

Interpreting Enum Values
====================

If you have an :ref:`object-type` or :ref:`action-type`\'s value, you can find out what that
number corresponds to using the ``convert_enum_value.py`` script.

.. code-block:: console

   python convert_enum.py <o|object|a|action> <number>

.. code-block:: console
   :caption: Example inputs/outputs

   python convert_enum.py object 1  # ObjectType.NONE
   python convert_enum.py a 1       # ActionType.MOVE_UP

Alternatively, you can use Python's `Interactive Mode <https://docs.python.org/3/tutorial/appendix.html#interactive-mode>`_:

.. code-block:: python

   python
   >>> from game.common.enums import *
   >>> ObjectType(<number>)

.. note::
   As long as you keep entering valid Python, you're basically writing a temporary Python script in your shell.
   If you wanted, you could even do
   
   .. code-block:: python

      >>> for i in range(1, 10):
      ...     ObjectType(i)

   This is a very powerful tool that can be used for much more than converting enums.
   For more information, see https://docs.python.org/3/tutorial/appendix.html#interactive-mode.

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
   :class: ghost
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

.. important::
   As commands are listed, some will have several versions that perform the same task. 

   Only **ONE** line needs to be typed into the terminal, **NOT** all.

Generate
--------

If you don't want to have a new, random seed, don't run this command. With the same seed and clients, the results will
stay consistent.

.. code-block:: console

   python launcher.pyz g
   python launcher.pyz gen
   python launcher.pyz generate

.. _run-command:

Run
---

As the game is running, any print statements you have will print to your console, which can be useful for
debugging. There will also be logs generated in the ``logs`` folder, showing what information was stored each turn in
the JSON format.

.. code-block:: console

   python launcher.pyz r
   python launcher.pyz run

Visualize
---------

This displays each turn of the game you ran, allowing you to debug in a more user-friendly way! How wonderful.
Visit :doc:`visualizer` for more details.

.. code-block:: console

   python launcher.pyz v
   python launcher.pyz vis
   python launcher.pyz visualize

Launcher Help
-------------

To see every possible command combination, run

.. code-block::

    python launcher.pyz -h

Some commands have their own help messages, which can be displayed via

.. code-block::

   python launcher.pyz <command> -h

Updating Your Launcher
=====================

Do **ONE** of the following:

- Pull from the client package repo's main	
- Save your client file(s) (any code that you wrote) and re-clone/redownload the client package repo (if the first solution didn't work; it's happened in the past)
