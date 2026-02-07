===============
Getting Started
===============


*ring* *ring* HELLO? HELLO, HELLO?!
===================================

*uuuuh* We wanted to type up a message for you to help you get settled in on your first night.

Prerequisites
===================================

- Python 3.13; download it `here <https://www.python.org/downloads/release/python-31312/>`_.
    - Python 3.14 **HAS** been tested and it does **BREAK** things. Please **DO NOT** use it.

- A code editor with Python support; some recommendations:
    - VS Code/`VSCodium <https://vscodium.com/#install>`_ with the Python extension published by **ms-python**
    - `PyCharm <https://www.jetbrains.com/pycharm/download/>`_


The Client Package
===================================

To begin patrolling the dark, dank halls of QBB, you must download the contents of `this repository <https://github.com/acm-ndsu/Byte-le-2026-Client-Package>`_.
You may do so in many ways... here are some:

Using `Git <https://git-scm.com/install>`_'s built-in CLI
$$$$$$$$$


1. In the directory you want to download to, run the following command:

.. code-block:: console

    git clone https://github.com/<user>/Byte-le-Engine-2026-Client-Package.git

Using `GitHub CLI <https://cli.github.com/>`_
$$$$$$$$$$$

1. In the directory you want to download to, run the following command:

.. code-block:: console

    gh repo clone <user>/Byte-le-2026-Client-Package

.. container:: centered
   :font-size: 48px

   ^^^^^^ **CHANGE USER**

Using `GitHub Desktop <https://desktop.github.com/download/>`_
$$$$$$$$$

1. Go to https://github.com/acm-ndsu/Byte-le-2026-Client-Package

2. Press the ``<> Code`` button to drop down a menu:

.. figure:: /_static/images/clone_repo.png
    :width: 60%
    :align: center

3. Press "Open with GitHub Desktop"
    i. Allow the website to open GitHub Desktop if you have it downloaded already
    ii. Once in GitHub Desktop, the URL to the repository will be provided
    iii. Choose where you'd like it saved on your device
    iv. Click ``Clone`` and you're good to go!

.. figure:: /_static/images/github_desktop.png
    :width: 70%
    :align: center

Download ZIP
$$$$$$$$$$$$

1. Go to https://github.com/acm-ndsu/Byte-le-2026-Client-Package

2. Press the ``<> Code`` button to drop down a menu:

.. figure:: /_static/images/clone_repo.png
    :width: 60%
    :align: center

3. Click ``Download ZIP`` and find it in your Downloads.
4. Extract the files somewhere on your device.

Installing Dependencies
===============

It's good practice to set up a virtual environment to separate Byte-le's packages
from any system-wide Python packages you might have installed.
For more information on Python virtual environments, go `here <https://docs.python.org/3/library/venv.html>`_.
In your project directory, run the following commands in a command line:

.. code-block:: console

    python -m venv .venv

To activate your virtual environment, run **one** of the following commands depending on your shell:

.. .. tabs::
..
..     .. group-tab:: cmd
..
..         .. code-block:: cmd
..
..            .\.venv\Scripts\activate.bat

.. code-block:: cmd
   :caption: cmd

   .\.venv\Scripts\activate.bat

..     .. group-tab:: PowerShell
..

.. code-block:: powershell
   :caption: PowerShell

    .\.venv\Scripts\Activate.ps1

..
..     .. group-tab:: Bash/zsh
..

.. code-block:: bash
    :caption: Bash/zsh

    source .venv/bin/activate
..
..     .. group-tab:: fish
..
.. code-block:: fish
    :caption: fish

    source .venv/bin/activate.fish



If you don't see your shell or these don't work, find the appropriate command for your shell `here <https://docs.python.org/3/library/venv.html#how-venvs-work>`_.

.. note::

    If your virtual environment was activated, your shell might notice, adding "``.venv``" somewhere in your prompt like so:

    .. .. tabs::

    ..    .. group-tab:: cmd

    .. code-block:: console
        :caption: cmd

        (.venv) C:\path\to\Byte-le-2026-Client-Package\>

    ..    .. group-tab:: PowerShell

    .. code-block:: console
        :caption: PowerShell

        (.venv) PS C:\path\to\Byte-le-2026-Client-Package\>

    ..    .. group-tab:: Bash/zsh

    .. code-block:: console
        :caption: Bash

        (.venv) /path/to/Byte-le-2026-Client-Package $

    ..    .. group-tab:: fish

    .. code-block:: fish
        :caption: fish

        .venv /path/to/Byte-le-2026-Client-Package >

    Alternatively, you can check your path to Python:

    .. .. tabs::

    ..    .. group-tab:: cmd

    .. code-block:: console
        :caption: cmd

        where.exe python

    ..    .. group-tab:: PowerShell

    .. code-block:: console
        :caption: PowerShell

        where.exe python

    ..    .. group-tab:: Bash/zsh

    .. code-block:: console
        :caption: Bash/zsh

        which python

    If your virtual environment is activated, the output of these commands should include a path that looks something like ``/path/to/Byte-le-2026-Client-Package/path/to/venv/bin/python``.


Once your virtual environment is activated, run the following command to install Byte-le's packages:

.. code-block:: console

    pip install -r requirements.txt

More useful commands are listed in :doc:`useful_commands`.


What Now?
=============

To learn more about the game mechanic's, read :doc:`HowToPlay`!

To get your team registered and learn how to submit your code, read :doc:`server`!

To learn how to make your lil' guy do stuff, read :doc:`controls`!

For tips on programming your client, read :doc:`tips`!

Submitting Issues
================

If you run into issues with the game, please submit an issue to the Discord server in the
`#bug-reporting channel <https://discord.com/channels/697995889020633221/1357477016269492375>`_
or call a developer over!

