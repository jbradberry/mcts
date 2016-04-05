from distutils.core import setup

setup(
    name='MonteCarloTreeSearch',
    version='0.1dev',
    author='Jeff Bradberry',
    author_email='jeff.bradberry@gmail.com',
    packages=['mcts'],
    entry_points={
        'jrb_board.players': ['jrb.mcts.uct = mcts.uct:MonteCarlo',
                              'jrb.mcts.uctv = mcts.uct:ValueMonteCarlo'],
    },
    license='LICENSE',
    description="An implementation of UCT Monte Carlo Tree Search.",
)
