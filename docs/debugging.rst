==========================
Debugging
==========================

The Visualizer
--------------

:doc:`visualizer` allows you to watch your client's actions play out in real-time (or faster)!
Note that the game is simply being "replayed" by the visualizer, so nothing will be printed by your
client.

Printing Turn Info
------------------

Everything you print in your client's ``take_turn()`` method will be printed on every turn it takes
while the game is running. See :ref:`run-command` to learn how to run the game locally.
This can be useful when paired with :doc:`visualizer`!

The Logs
--------

Whenever you run a game, a ``logs`` folder will be created. This folder contains a
``.json`` file for every turn and stores the information about the game world during that turn.
If you're wondering what the value of a stored :ref:`object-type` or :ref:`action-type` means,
see :ref:`enum-script`.

point data
