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

For your convenience:

.. code-block:: python

   import heapq
   from typing import Dict, List, Tuple, Optional
   from game.common.enums import ActionType, ObjectType
   from game.common.game_object import GameObject
   from game.common.map.occupiable import Occupiable
   from game.constants import DIRECTION_TO_MOVE
   from game.utils.vector import Vector

   Position = Tuple[int, int]

   DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]


   def a_star_move(start: Vector, goal: Vector, world, allow_vents: bool = True, game_object: GameObject | None = None) -> ActionType | None:
       path = a_star_path(
           start=start,
           goal=goal,
           world=world,
           allow_vents=allow_vents, 
           game_object=game_object
       )

       if not path or len(path) < 2:
           return None

       next_step: Vector = path[1]
       direction = next_step - start
       action = DIRECTION_TO_MOVE.get(direction)
       return action

   def a_star_path(start: Vector, goal: Vector, world, allow_vents = True, game_object: GameObject | None = None) -> Optional[List[Vector]]:
       start_p = (start.x, start.y)
       goal_p = (goal.x, goal.y)

       frontier = [(0, start_p)]
       came_from = {start_p: None}
       cost = {start_p: 0}

       while frontier:
           _, current = heapq.heappop(frontier)

           if current == goal_p:
               path = []
               while current is not None:
                   x, y = current
                   path.insert(0, Vector(x, y))
                   current = came_from[current]
               return path

           for dx, dy in DIRECTIONS:
               nxt = (current[0] + dx, current[1] + dy)
               vec = Vector(nxt[0], nxt[1])

               if game_object is not None and not world.can_object_occupy(vec, game_object):
                   continue

               if not world.is_valid_coords(vec):
                   continue

               top = world.get_top(vec)
               if top and top.object_type != ObjectType.AVATAR:
                   # walls block
                   if top.object_type == ObjectType.WALL:
                       continue

                   # vents block unless allowed
                   if top.object_type == ObjectType.VENT and not allow_vents:
                       continue

                   # can't pass through non-occupiable
                   if not isinstance(top, Occupiable):
                       continue

               new_cost = cost[current] + 1
               if nxt not in cost or new_cost < cost[nxt]:
                   cost[nxt] = new_cost
                   priority = new_cost + vec.distance(goal)
                   heapq.heappush(frontier, (priority, nxt))
                   came_from[nxt] = current

       return None

