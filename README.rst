Monte Carlo Tree Search
=======================

This is an implementation of an AI in Python using the UCT Monte Carlo
Tree Search algorithm.

The Monte Carlo Tree Search AIs included here are designed to work
with `jbradberry/boardgame-socketserver
<https://github.com/jbradberry/boardgame-socketserver>`_ and
`jbradberry/boardgame-socketplayer
<https://github.com/jbradberry/boardgame-socketplayer>`_.


Requirements
------------

You need to have the following system packages installed:

* Python >= 2.7


Getting Started
---------------

To set up your local environment you should create a virtualenv and
install everything into it. ::

    $ mkvirtualenv mcts

Pip install this repo, either from a local copy, ::

    $ pip install -e mcts

or from github, ::

    $ pip install git+https://github.com/jbradberry/mcts#egg=mcts

Additionally, you will need to have `jbradberry/boardgame-socketplayer
<https://github.com/jbradberry/boardgame-socketplayer>`_ installed in
order to make use of the players.

This project currently comes with two different Monte Carlo Tree
Search players.  The first, ``jrb.mcts.uct``, uses the count of the
number of wins for a node to make its decisions.  The second,
``jrb.mcts.uctv`` instead keeps track of the evaluated value of the
board for the playouts from a given node ::

    $ board-play.py t3 jrb.mcts.uct    # number of wins metric
    $ board-play.py t3 jrb.mcts.uctv   # point value of the board metric

These AI players can also take additional arguments:

time
  The amount of thinking time allowed for the AI to make its decision,
  in seconds (default: 30).  Ex: ``$ board-play.py t3 jrb.mcts.uct -e
  time=5``

max_actions
  The maximum number of actions, or plays, to allow in one of the
  simulated playouts before giving up (default: 1000).  Ex: ``$
  board-play.py t3 jrb.mcts.uct -e max_actions=500``

C
  The exploration vs. exploitation coefficient at the heart of the UCT
  algorithm (default: 1.4).  Larger values prioritize exploring
  inadequately covered actions from a node, smaller values prioritize
  exploiting known higher valued actions.  Experimentation with this
  variable to find reasonable values for a given game is recommended.
  Ex: ``$ board-play.py t3 jrb.mcts.uct -e C=3.5``

The ``-e`` flag may be used multiple times to set additional
variables.

Games
-----

Compatible games that have been implemented include:

* `Reversi <https://github.com/jbradberry/reversi>`_
* `Connect Four <https://github.com/jbradberry/connect-four>`_
* `Ultimate (or 9x9) Tic Tac Toe
  <https://github.com/jbradberry/ultimate_tictactoe>`_
* `Chong <https://github.com/jbradberry/chong>`_
