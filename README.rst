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

* Python 2.7, 3.5+; PyPy; PyPy3
* six


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

time (default: 30)
  The amount of thinking time allowed for the AI to make its decision,
  in seconds.  Ex: ``$ board-play.py t3 jrb.mcts.uct -e time=5``

max_actions (default: 1000)
  The maximum number of actions, or plays, to allow in one of the
  simulated playouts before giving up.  Ex: ``$ board-play.py t3
  jrb.mcts.uct -e max_actions=500``

C (default: 1.4)
  The exploration vs. exploitation coefficient at the heart of the UCT
  algorithm.  Larger values prioritize exploring inadequately covered
  actions from a node, smaller values prioritize exploiting known
  higher valued actions.  Experimentation with this variable to find
  reasonable values for a given game is recommended.  Ex: ``$
  board-play.py t3 jrb.mcts.uct -e C=3.5``

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


Implementing New Games
----------------------

In order to create a compatible implementation of a board game, you
need to implement a class with the following methods::

    class BoardGame:
        def starting_state(self):
            # This method will be called by boardgame-socketserver or other server
            #
            # return value: tuple of ints (or some other simple Python built-in)

        def display(self, state, action, **kwargs):
            # This method will be called by boardgame-socketplayer or
            # other clients to obtain a console printable
            # representation of the board.
            #
            # state: nested dict, as returned by to_json_state
            # action: dict, as returned by to_json_action
            #
            # return value: unicode string

        def to_compact_state(self, data):
            # This method turns a nested dict (as sent over the wire
            # as a json object) into a compact representation of the
            # state of the game.  This compact state is then managed
            # as part of the game history, and is used internally by mcts.
            #
            # data: nested dict, as returned by to_json_state
            #
            # return value: tuple of ints, as returned by starting_state

        def to_json_state(self, state):
            # This method turns the internal representation of a state
            # into an object suitable to send over the wire between
            # client and server.
            #
            # state: tuple of ints
            #
            # return value: nested dict

        def to_compact_action(self, action):
            # action: dict
            #
            # return value: tuple

        def to_json_action(self, action):
            # action: tuple
            #
            # return value: dict

        def from_notation(self, notation):
            # notation: unicode string
            #
            # return value: tuple

        def to_notation(self, action):
            # action: tuple
            #
            # return value: unicode string

        def next_state(self, history, action):
            # history: list of states (tuples of ints)
            # action: tuple
            #
            # return value: tuple of ints

        def is_legal(self, state, action):
            # state: tuple of ints
            # action: tuple
            #
            # return value: bool

        def legal_actions(self, state):
            # state: tuple of ints
            #
            # return value: list of tuples (compact version of actions)

        def previous_player(self, state):
            # state: tuple of ints
            #
            # return value: int

        def current_player(self, state):
            # state: tuple of ints
            #
            # return value: int

        def is_ended(self, state):
            # state: tuple of ints
            #
            # return value: bool

        def win_values(self, state):
            # state: tuple of ints
            #
            # return value: dict or None

        def points_values(self, state):
            # state: tuple of ints
            #
            # return value: dict or None

        def winner_message(self, winners):
            # winners: dict
            #
            # return value: unicode string


Additionally, you need to register your new game class so that it can
be used.  To do this, add at least one entry point in your setup.py
file under the ``jrb_board.games`` namespace::

    setup(
        ...
        entry_points={
            'jrb_board.games': 'my_game = my_package.my_module:BoardGame',
        },
        ...
    )


Then when your package is installed, it will be ready to be used by
boardgame-socketserver, boardgame-socketplayer, and mcts.
