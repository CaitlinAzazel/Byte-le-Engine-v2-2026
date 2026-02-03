==========
The Visualizer
==========

The visualizer is a useful tool that will show you what actually happens in a game.

The Screen
==========

.. image:: ./_static/images/full_visualizer.png

The scores are above the top left and top right corners displaying the game with the characters. The turn counter
is centered on the top.

Active Character Indicator
==========================

To tell which character is taking their turn, an indicator will appear next to their headshot for that turn.


.. figure:: ./_static/images/active.png
    :width: 150

    The indicator to show which character is taking their turn.

.. figure:: ./_static/images/active_char.png
    :width: 550

    The indicator next to a character's headshot.


Controls
========

In the bottom middle of the screen there are buttons that will control playback of the game.

.. csv-table::
   :header-rows: 1
    
    Button, Function
    Pause,  Pauses or unpauses depending on the current state
    Prev,   Rewinds to the previous turn and pauses
    Next,   Proceeds to the next turn and pauses
    Start,  Rewinds to the first turn and pauses
    End,    Skips to the end of the game to instantly reveal the winner
    Speed,  Adjusts the playback speed of the visualizer. The default speed is 1x.
    Save,   Saves a .mp4 video file of the game in your root directory folder.
