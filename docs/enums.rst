=====
Enums
=====

Enums can represent a wide variety of things. Here is a list of enums and what they represent.

ActionType
==========

Things your character can do. For further details, see :doc:`controls`.

.. csv-table:: 

    NONE, Do nothing
    MOVE_UP, Move up one tile
    MOVE_DOWN, Move down one tile
    MOVE_LEFT, Move left one tile
    MOVE_RIGHT, Move right one tile
    INTERACT_UP, Interact with the tile above you
    INTERACT_DOWN, Interact with the tile below you
    INTERACT_LEFT, Interact with the tile to your left
    INTERACT_RIGHT, Interact with the tile to your right
    INTERACT_CENTER, Interact with the tile you are standing on

ObjectType
==========

Things in the game. Note the difference between ``SCRAP_ITEM`` and ``SCRAP_SPAWNER``.

.. csv-table::

   SCRAP_ITEM, Scrap that you have collected
   SCRAP_SPAWNER, A tile where you can collect ``SCRAP``
   BATTERY_SPAWNER, A tile where you can collect batteries that restore power
   COIN_SPAWNER, A tile where you can collect coins that give you points
   GENERATOR, A generator; fueled by ``SCRAP``
   VENT, A vent
   REFUGE, A tile that bots cannot enter
   DOOR, A door; opened by generators
   CRAWLER_BOT, **REDACTED**
   DUMB_BOT, **REDACTED**
   IAN_BOT, **REDACTED**
   JUMPER_BOT, **REDACTED**
   SUPPORT_BOT, **REDACTED**

Reading Logs
------------
If you are looking at an "object_type" in log files, it will be a number.
If you want to know what that number corresponds to, run the following commands:

.. code-block:: python

   python
   >>> from game.common.enums import *
   >>> ObjectType(<number>) # should print something

.. note::
   We are using Python's **R**\ead **E**\valuate **P**\rint **L**\oop here.
   As long as you keep entering valid Python, you're basically writing a temporary Python script in your shell.
   So, if you wanted, you could even do
   
   .. code-block:: python

      >>> for i in range(1, 10):
      ...     ObjectType(i)

   For more information, see https://docs.python.org/3/tutorial/appendix.html#interactive-mode
