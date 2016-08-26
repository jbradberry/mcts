Monte Carlo Tree Search
=======================

This is an implementation of an AI in Python using the UCT Monte Carlo
Tree Search algorithm.


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

The Monte Carlo Tree Search AIs included here are designed to work
with `jbradberry/boardgame-socketserver
<https://github.com/jbradberry/boardgame-socketserver>`_ and
`jbradberry/boardgame-socketplayer
<https://github.com/jbradberry/boardgame-socketplayer>`_.


Games
-----

Compatible games that have been implemented include:

* `Reversi <https://github.com/jbradberry/reversi>`_
* `Connect Four <https://github.com/jbradberry/connect-four>`_
* `Ultimate (or 9x9) Tic Tac Toe
  <https://github.com/jbradberry/ultimate_tictactoe>`_
* `Chong <https://github.com/jbradberry/chong>`_
