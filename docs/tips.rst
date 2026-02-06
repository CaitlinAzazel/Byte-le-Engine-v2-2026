===============
Tips & Tricks
===============

Strategy Tips
=============

* Prioritize collecting Scrap early to unlock generators
* Unlocking areas increases your multiplier and your escape options
* Do not hoard Scrap too long, as locked areas limit your movement
* Learn bot movement patterns to avoid being trapped
* Higher multipliers mean higher risk but higher reward

Programming Tips
================

.. |discord| raw:: html

   <a href="https://discord.com/channels/697995889020633221/1357476969461059595" target="_blank">Official Byte-le Royale Server</a>

When in doubt:
   - https://docs.python.org/3.13/
   - https://www.w3schools.com/python/default.asp
   - |discord|

.. note::
   For brevity, variables representing ``Vector`` s are written as ``<variable_name>``.

Want to go somewhere? Use ``convert_vector_to_move(...)`` (from ``game.constants``)

.. code-block:: python

   # I want to go to <goal> but I'm at <position>!
   move_action: ActionType = convert_vector_to_move(goal - position)

Want to interact with something? Use ``convert_vector_to_interact(...)`` (from ``game.constants``)

.. code-block:: python

   # I want to interact with something <there> but I'm <here>!
   interact_action: ActionType = convert_vector_to_interact(there - here)

Want to know if you can stand in a certain spot? Use ``GameBoard.can_object_occupy(...)``

.. code-block:: python
   :caption: Given that ``game_board`` is a ``GameBoard`` and ``my_avatar`` is an ``Avatar``

   # Can I stand <over_there>?
   can_stand_over_there = game_board.can_object_occupy(over_there, my_avatar)

Want to know how much points something gives? Look for properties mentioning a "bonus" or "points":

.. csv-table::
   :header: Property, Meaning

   ``Generator.activation_bonus``, The amount of points granted upon your **FIRST** time activating that specific generator (varies between instances)
   ``Generator.multiplier_bonus``, The amount that your multiplier is increased **WHILE** this ``Generator.is_active``
   ``CoinSpawner.point_value``, The amount of points granted for collecting a coin from this instance
   ``ScrapSpawner.point_value``, Similar to ``CoinSpawner.point_value``
   ``BatterySpawner.point_value``, Similar to ``CoinSpawner.point_value``

