=====
Enums
=====

Enums can represent a wide variety of things. Here is a list of enums and what they represent.

See :ref:`enum-script` for more on how to interpret enums as seen in log files.

.. _action-type:

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

.. _object-type:

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
   CRAWLER_BOT, ████████ █████
   DUMB_BOT, ██ █████ ██████ ██ 
   IAN_BOT, "█████, █████ ███ "
   JUMPER_BOT, ████ ████ 
   SUPPORT_BOT, ████████; █████ ███ 

