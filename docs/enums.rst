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
   :class: ghost

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
   :class: sprite

.. |battery| image:: /_static/images/battery.png
   :scale: 100%
   :class: sprite

.. |coin| image:: /_static/images/coin.png
   :scale: 100%
   :class: sprite

.. |generator| image:: /_static/images/generator.png
   :scale: 100%
   :class: sprite

.. |vent| image:: /_static/images/vent_door.png
   :scale: 100%
   :class: sprite

.. |refuge| image:: /_static/images/safe_spot_open.png
   :scale: 100%
   :class: sprite

.. |door| image:: /_static/images/door_closed.png
   :scale: 100%
   :class: sprite

.. |cables| image:: /_static/images/cables.png
   :scale: 100%
   :class: sprite

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

.. |avatar| image:: /_static/images/and_you_the.png
   :scale: 100%
   :class: sprite

.. csv-table::
   :class: ghost

   ,SCRAP_ITEM, Scrap that you have collected,
   |scrap|,SCRAP_SPAWNER, A tile where you can collect ``SCRAP``
   |battery|,BATTERY_SPAWNER, A tile where you can collect batteries that restore power
   |coin|,COIN_SPAWNER, A tile where you can collect coins that give you points
   |generator|,GENERATOR, A generator; fueled by ``SCRAP``
   |vent|,VENT, A vent; big enough for you to *crawl* through
   |refuge|,REFUGE, "A tile that bots cannot enter; ejects humans that stay inside it too long"
   |door|,DOOR, A door; opened by generators
   |avatar|, AVATAR, You!
   |cables|,CRAWLER_BOT, ████████ █████
   |bison|,DUMB_BOT, ██ █████ ██████ ██ 
   |e_n|,IAN_BOT, "█████, █████ ███ "
   |deer|,JUMPER_BOT, ████ ████ 
   |trash_heap|,SUPPORT_BOT, ████████; █████ ███ 

*Psst... want to know more about the animatronics? There's declassified info in* :ref:`bot-quirks`
