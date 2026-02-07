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

.. _bot-quirks:

Bot Quirks
==========

The animatronics seem to be a bit quirky:

.. |cables| image:: /_static/images/cables.png
   :scale: 100%

.. |bison| image:: /_static/images/bison.png
   :scale: 100%
   :class: sprite

.. |e_n| image:: /_static/images/e_n.png
   :scale: 100%
   :class: sprite

.. |deer| image:: /_static/images/deer.png
   :scale: 100%
   :class: sprite

.. |trash_heap| image:: /_static/images/trash_heap_on.png
   :scale: 100%
   :class: sprite

.. csv-table::
   :class: ghost

   |cables|, Crawler, "Always knows where you are, is slow, can enter vents"
   |bison|, Thundar, "Has poor eyesight, moves erratically"
   |e_n|, I.A.N., "Always knows where you are, is fast"
   |deer|, Doe/Jumper, "Moves diagonally"
   |trash_heap|, Computer?, "Turns on after some time, other bots get quirkier while it's on"


Programming Tips
================

.. |discord| raw:: html

   <a href="https://discord.com/channels/697995889020633221/1357476969461059595" target="_blank">Official Byte-le Royale Server</a>

When in doubt:
   - https://docs.python.org/3.13/
   - https://www.w3schools.com/python/default.asp
   - |discord|

.. note::
   For brevity, variables representing ``Vector`` s are written as ``<variable_name>`` in the following code examples.

Generators
----------

You can check the scrap cost of a generator via ``Generator.cost`` 

Navigation
----------

Want to know if you can stand in a certain spot?
Use ``GameBoard.can_object_occupy(...)``

.. code-block:: python
   :caption: Given that ``game_board`` is a ``GameBoard`` and ``my_avatar`` is an ``Avatar``

   # Can I stand <over_there>?
   can_stand_over_there: bool = game_board.can_object_occupy(over_there, my_avatar)

Want to move somewhere?
Use ``convert_vector_to_move(...)`` (from ``game.constants``)

.. code-block:: python

   # I want to go to <goal> but I'm at <position>!
   move_action: ActionType | None = convert_vector_to_move(goal - position)

Want to interact with something?
Use ``convert_vector_to_interact(...)`` (from ``game.constants``)

.. code-block:: python

   # I want to interact with something <there> but I'm <here>!
   interact_action: ActionType | None = convert_vector_to_interact(there - here)

.. caution::
   Be mindful that the above two functions can return ``None``.
   See :ref:`walking-touching` for a more detailed explanation.

Want to know everything that occupies a certain spot?

.. code-block:: python

   # What's over <there>?
   game_objects: GameObjectContainer | None = world.get(there)

.. important::
   ``GameObjectContainer`` is a custom data structure.
   You may have to do some more digging to find what you're looking for.

Want to know everything **of a certain type** that occupies a certain spot?

.. code-block:: python

   # Are there any BatterySpawners over <there>?
   game_objects: list[GameObject] = world.get_objects_from(there, ObjectType.BATTERY_SPAWNER)

Points
--------------

Want to know how much points something gives? Look for properties mentioning a "bonus" or "points":

.. csv-table::
   :class: ghost
   :header: Property, Meaning

   ``Generator.activation_bonus``, The amount of points granted upon your **FIRST** time activating that specific generator (varies between instances)
   ``Generator.multiplier_bonus``, The amount that your multiplier is increased **WHILE** this ``Generator.is_active``
   ``CoinSpawner.point_value``, The amount of points granted for collecting a coin from this instance
   ``ScrapSpawner.point_value``, Similar to ``CoinSpawner.point_value``
   ``BatterySpawner.point_value``, Similar to ``CoinSpawner.point_value``

Vectors
--------------

Want to know how far away something is?
Use ``Vector.distance(...)``

.. code-block:: python

   # How far is <here> from <there>?
   distance: int = here.distance(there)

Only need to know if something is closer/farther?
Use ``Vector.is_closer_to(...)``/``Vector.is_farther_from(...)``

.. important::
   These methods return ``False`` if the positions are **equally** close/far.

.. code-block:: python

   # Is <here> closer to <somewhere> than <there>?
   is_closer: bool = here.is_closer_to(somewhere, there)
   # Is <here> farther from <somewhere> than <there>?
   is_closer: bool = here.is_farther_from(somewhere, there)

Want to know what positions are between two points?
Use ``Vector.get_positions_overlapped_by_line(...)``

.. note::
   This function uses `Bresenham's line algorithm <https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#>`_.

.. code-block:: python

   # What are the places between <here> and <there>?
   places = Vector.get_positions_overlapped_by_line(here, there)
