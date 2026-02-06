========================
Controlling your Avatar
========================


Actions List
============

Your ``Client.take_turn()`` method *must* return a list of ``ActionType`` s.
Note that only the **FIRST TWO** actions will be actually be used by the engine.

See :doc:`enums` for a list of all possible ``ActionType`` s.

.. note::
   You may see additional ``ActionTypes`` s in your editor's autocomplete, but those ``ActionType`` s will not do anything.


.. _walking-touching:

Walking Around And Touching Stuff
==============

To collect coins, batteries, and scrap, all you have to do is walk onto them. No interaction required.

Once you have a direction you want to move or interact, you can use ``convert_vector_to_move()`` or ``convert_vector_to_interact()`` to get a corresponding ``ActionType``. These functions (and other useful stuff) can be imported from ``game.constants``.

.. caution::
   If a conversion fails, these functions will return None.
   This might happen if you convert "diagonal" vectors
   because you can only move and interact straight up/down/left/right:

   .. code-block:: python
      
      convert_vector_to_move(Vector(6, 7))       # None
      convert_vector_to_interact(Vector(-9, -9)) # None
      convert_vector_to_move(Vector(1, 0))       # ActionType.MOVE_RIGHT
      convert_vector_to_interact(Vector(0, 0))   # ActionType.INTERACT_CENTER

   Additionally, you cannot convert a zero vector to a move because... well... you can figure that out.

   You can, however, convert a zero vector to an interact because you can interact with the tile you're standing on. :^)

.. note::
   Moving "up" is actually moving in a negative y direction. Strange.

Activating Generators
=====================

If you have enough scrap, you may activate a generator by interacting with it.
Since you must use ``ActionType`` s, you must also know which direction to interact:

.. caution::
   You may only interact with the tile you stand on and those directly above, below, left, or right of you.

.. code-block:: python

     # x.direction_to(y) returns (y - x).as_direction()
     direction_to_generator = avatar.position.direction_to(generator_position)
     # DIRECTION_TO_INTERACT and other useful lookup tables
     # can be imported from game.constants
     interact_action = DIRECTION_TO_INTERACT.get(direction_to_generator)
     if interact_action is None:
         # the generator is not directly up/down/left/right
     else:
         actions.append(interact_action)


Pathfinding
============

something something
