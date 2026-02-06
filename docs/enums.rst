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

.. |scrap| image:: /_static/images/scrap.png
   :scale: 100%

.. |battery| image:: /_static/images/battery.png
   :scale: 100%

.. |coin| image:: /_static/images/coin.png
   :scale: 100%

.. |generator| image:: /_static/images/generator.png
   :scale: 100%

.. |vent| image:: /_static/images/vent_door.png
   :scale: 100%

.. |refuge| image:: /_static/images/safe_spot_open.png
   :scale: 100%

.. |door| image:: /_static/images/door_closed.png
   :scale: 100%

.. |cables| image:: /_static/images/cables.png
   :scale: 100%

.. |bison| image:: /_static/images/bison.png
   :scale: 100%

.. |e_n| image:: /_static/images/e_n.png
   :scale: 100%

.. |deer| image:: /_static/images/deer.png
   :scale: 100%

.. |trash_heap| image:: /_static/images/trash_heap_on.png
   :scale: 100%

.. csv-table::

   ,SCRAP_ITEM, Scrap that you have collected,
   |scrap|,SCRAP_SPAWNER, A tile where you can collect ``SCRAP``
   |battery|,BATTERY_SPAWNER, A tile where you can collect batteries that restore power
   |coin|,COIN_SPAWNER, A tile where you can collect coins that give you points
   |generator|,GENERATOR, A generator; fueled by ``SCRAP``
   |vent|,VENT, A vent; small enough for you to *crawl* through
   |refuge|,REFUGE, A tile that bots cannot enter
   |door|,DOOR, A door; opened by generators
   |cables|,CRAWLER_BOT, ████████ █████
   |bison|,DUMB_BOT, ██ █████ ██████ ██ 
   |e_n|,IAN_BOT, "█████, █████ ███ "
   |deer|,JUMPER_BOT, ████ ████ 
   |trash_heap|,SUPPORT_BOT, ████████; █████ ███ 

