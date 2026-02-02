===============
Getting Started
===============

*RING* *RING* HELLO? HELLO HELLO?!
==========================

*uuuh* I wanted to type up a message for you to help you get settled in on your first night.

It's good practice to set up a virtual environment to separate Byte-le's packages
from any system-wide packages you might have installed.
For more information on Python virtual environments, go `here <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/>`_.
In your project directory, run the following commands in a command line:

.. code-block:: console

    python -m venv .venv

To activate your virtual environment, run **one** of the following commands depending on your shell:

.. code-block:: powershell
   :caption: cmd/PowerShell

    .\.venv\Scripts\activate

.. code-block:: bash
   :caption: bash/zsh

    source .venv/bin/activate

If these didn't work, find the appropriate command for your shell `here <https://docs.python.org/3/library/venv.html#how-venvs-work>`_.

Once your virtual environment is activated, run the following command to install Byte-le's packages:

.. code-block:: console

    pip install -r requirements.txt

More useful commands are listed in :doc:`useful_commands`.


Objective
=========

Your objective is to create the perfect team of three mercenaries to defeat your opponents within 350 turns and claim
victory over the battle. Your team will consist of two generic soldiers and one leader. Each character has a special
set of Moves. When executing their turn, they can choose one of these Moves to use. Some of these Moves may cost
special points to use, which is gathered by using their Normal Move. Each character will also have their own
stats, including their current health, max health, attack, speed, and defense.

You can find more information on :doc:`characters`, as well as :doc:`stats` and :doc:`moves` in their respective pages.

Tournament Structure
====================

Each pairing of teams will have one game against each other. The points gained from that game
will be added to those teams' total points in the tournament.

For more information on tournament structure and scoring, please visit :doc:`scoring`.

Running the Game
================


Python Version
--------------

Make sure to uninstall the Visual Studio Code version of Python if you have Visual Studio Code installed.
You can do this by re-running the installer and unselecting the Python development kit then clicking update.

:gold:`We require using Python version 3.12.` You can go to the
`official Python website <https://www.python.org/downloads/release/python-3125/>`_ to download it.

You can use any text editor or IDE for this competition, but we recommend Visual Studio Code.

Getting the Code and your Team
------------------------------

To receive the code and to begin commanding your own team of mercenaries, please clone the repository
`here <https://github.com/acm-ndsu/Byte-le-2025-Client-Package>`_.

When on GitHub, press the green ``<> Code`` button to drop down the menu:

.. image:: /images/clone_repo.png

We highly recommend cloning with GitHub Desktop or downloading the ZIP folder. Extra props if you can use the terminal!

#. Open with GitHub Desktop
    * Allow the website to open GitHub Desktop if you have it downloaded already
    * Once in GitHub Desktop, the URL to the repository will be provided
    * Choose where you'd like it saved on your device
    * Click ``Clone`` and you're good to go!

.. image:: /images/github_desktop.png

#. Download ZIP
    * Click ``Download ZIP`` and find it in your Downloads.
    * Extract the files and save it somewhere on your device.
    * Use your IDE/text editor (Visual Studio Code is recommended) of choice and open the extracted folder downloaded.
    * You're ready to code!


Submitting Code
---------------

To submit your code, command your team in either your ``base_client.py`` or ``base_client_2.py`` files. When you submit
your code via the command specified in :doc:`server`, you can submit either of these files if you choose to.


Submitting Issues
-----------------

If you run into issues with the game, please submit an issue to the discord in the bugs channel or call a developer
over!
