from __future__ import absolute_import
from distutils.core import setup

setup(
    name='MonteCarloTreeSearch',
    version='0.1dev',
    author='Jeff Bradberry',
    author_email='jeff.bradberry@gmail.com',
    packages=['mcts'],
    entry_points={
        'jrb_board.players': ['jrb.mcts.uct = mcts.uct:UCTWins',
                              'jrb.mcts.uctv = mcts.uct:UCTValues'],
    },
    install_requires=['six'],
    license='LICENSE',
    description="An implementation of UCT Monte Carlo Tree Search.",
)
