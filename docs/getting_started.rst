===============
Getting Started
===============


*ring* *ring* HELLO? HELLO, HELLO?!
===================================

*uuuuh* We wanted to type up a message for you to help you get settled in on your first night.

Prerequisites
===================================

- Python 3.13; Download it `here <https://www.python.org/downloads/release/python-31311/>`_.

- A code editor with Python support; some recommendations:
    - VS Code/`VSCodium <https://vscodium.com/#install>`_ with the Python extension published by ms-python
    - `PyCharm <https://www.jetbrains.com/pycharm/download/>`_


The Client Package
===================================

To begin patrolling the dark, dank halls of QBB, you must download the contents of `this repository <https://github.com/acm-ndsu/Byte-le-2025-Client-Package>`_.
You may do so in many ways... here are some:

Using `Git <https://git-scm.com/install>`_'s built-in CLI
$$$$$$$$$


#. In the directory you want to download to, run the following command:

.. code-block:: console

    git clone https://github.com/<user>/Byte-le-Engine-2026-Client-Package.git

Using `GitHub CLI <https://cli.github.com/>`_
$$$$$$$$$$$

#. In the directory you want to download to, run the following command:

.. code-block:: console

    gh repo clone <user>/Byte-le-2026-Client-Package

.. container:: centered
   :font-size: 48px

   ^^^^^^ **CHANGE USER**

Using `GitHub Desktop <https://desktop.github.com/download/>`_
$$$$$$$$$

#. Go to https://github.com/acm-ndsu/Byte-le-2025-Client-Package

#. Press the ``<> Code`` button to drop down a menu:

.. container:: centered

    .. image:: /images/clone_repo.png
        :width: 60%

2. Press "Open with GitHub Desktop"
    * Allow the website to open GitHub Desktop if you have it downloaded already
    * Once in GitHub Desktop, the URL to the repository will be provided
    * Choose where you'd like it saved on your device
    * Click ``Clone`` and you're good to go!

.. container:: centered

    .. image:: /images/github_desktop.png
        :width: 70%

Download ZIP
$$$$$$$$$$$$

#. Go to https://github.com/acm-ndsu/Byte-le-2025-Client-Package

#. Press the ``<> Code`` button to drop down a menu:

.. container:: centered

    .. image:: /images/clone_repo.png
        :width: 60%

#. Click ``Download ZIP`` and find it in your Downloads.
#. Extract the files somewhere on your device.

Installing Dependencies
===============

It's good practice to set up a virtual environment to separate Byte-le's packages
from any system-wide Python packages you might have installed.
For more information on Python virtual environments, go `here <https://docs.python.org/3/library/venv.html>`_.
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

If you didn't see your shell or these didn't work, find the appropriate command for your shell `here <https://docs.python.org/3/library/venv.html#how-venvs-work>`_.

Once your virtual environment is activated, run the following command to install Byte-le's packages:

.. code-block:: console

    pip install -r requirements.txt

More useful commands are listed in :doc:`useful_commands`.


What Now?
---------------

To learn how to get your lil' guy movin' around, read :doc:`controls`!

To get your team registered and learn how to submit your code, read :doc:`the_server`!

Submitting Issues
-----------------

If you run into issues with the game, please submit an issue to the Discord server in the
`#bug-reporting channel <https://discord.com/channels/697995889020633221/1357477016269492375>`_
or call a developer over!
