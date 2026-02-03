=====
Enums
=====

Enums can represent a wide variety of things. Here is a list of different enums and what they represent.

ActionType
----------

Things your character can do. For further details, see :doc:`actions`.

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
----------

Things in the game. Note the difference between ``SCRAP`` and ``SCRAP_SPAWNER``.

.. csv-table::

   GENERATOR, A generator; fueled by ``SCRAP``
   SCRAP, Scrap that you have collected
   SCRAP_SPAWNER, A tile where you can collect ``SCRAP``
   VENT, A vent
   BATTERY, "A tile where you can collect batteries that restore power"
   REFUGE, A tile that bots cannot enter
   DOOR, A door; opened by generators
   COIN, A tile where you can collect coins that give you points
   CRAWLER_BOT, **REDACTED**
   DUMB_BOT, **REDACTED**
   IAN_BOT, **REDACTED**
   JUMPER_BOT, **REDACTED**
   SUPPORT_BOT, **REDACTED**

