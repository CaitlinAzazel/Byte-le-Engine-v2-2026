==========
The Server
==========


Code Time-Outs
==============

Every team is allowed a maximum of 0.1 seconds for their code to execute. If one of your submissions takes longer than the allowed time, that submission will be disqualified. This is to ensure the competition runs smoothly and pushes
competitors to write efficient code. Good luck, and think hard!

Client Commands
===============

.. important::
   As commands are listed, some will have two versions to perform the same task. The first command will be typed in its entirety, and the second command will be a shortened version for ease of use.

   Only **ONE** line needs to be typed into the terminal, **NOT** both.

Registering
----------

To register your team, run

.. code-block::

    python launcher.pyz client register

Follow the prompts to enter your team name, select your university, and select if you are an alumni.

After registering, you will receive a new file called ``vID`` in your root folder.

.. danger:: DO **NOT** SHARE YOUR vID. THE ANIMATRONICS WILL **GET** YOU.

This is unique to your team and allows you to submit clients and view your team's information.


Submitting Code
---------------

.. code-block::

    python launcher.pyz client submit
    python launcher.pyz c submit


After successfully registering your team, you are able to submit your client code. At least one client must be
submitted before the end of the competition to be eligible to win. We recommend that you at least submit the provided ``base_client.py``.
Additionally, any additional clients that you write should (1) have the ``.py`` extension, (2) contain the word "client" in the filename, and (3) be saved in the root of your package directory so that they can be detected by the launcher.

.. note::
   If your client file does not satisfy the above criteria, you can manually enter a **relative** (based on the package directory) path to your file when prompted by the launcher.

.. important::
   Your client file cannot import any modules that you create locally; ALL of the logic for your client must be contained in your client file. Sorry!

Once uploaded to the server, your bot will run against other submitted bots to determine placing. You can submit as
many times as you'd like during the duration of the competition, but please do not excessively submit.


Leaderboard
-----------

.. code-block::

    python launcher.pyz client leaderboard
    python launcher.pyz c l

These will return the leaderboard for all eligible contestants. By default, alumni are not included. To include
alumni, type one of the following:

.. code-block::

    python launcher.pyz client leaderboard -include_alumni
    python launcher.pyz c l -include_alumni

If you want to see previous leaderboards from the competition, you may type one of the following by providing a
leaderboard's id:

.. code-block::

    python launcher.pyz client leaderboard -leaderboard_id <leaderboard_id>
    python launcher.pyz c l -leaderboard_id <leaderboard_id>


Stats
-----

To view your stats for the latest submission, type one of the following:

.. code-block::

    python launcher.pyz client stats
    python launcher.pyz c s

Your stats will continue to change until all games are completed.

If you desire to see all of your submissions, type

.. code-block::

    python launcher.pyz client stats -get_submissions
    python launcher.pyz c s -get_submissions

to receive all your submission ids. These ids can be used in some of the commands listed below.

To receive code from a previous submission, have a submission id ready and type

.. code-block::

    python launcher.pyz client stats -get_code_for_submission <submission_id>
    python launcher.pyz c s -get_code_for_submission <submission_id>

to receive the code file from the given submission.


Extra Help
==========

For extra help on these commands, you can type ``-h`` after any of these commands to have the help message appear.
For example:

.. code-block::

    python launcher.pyz client -h
    python launcher.pyz c -h

or

.. code-block::

    python launcher.pyz client leaderboard -h
    python launcher.pyz c l -h

will show you the help descriptions of all client and leaderboard commands respectively.

