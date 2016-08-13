from __future__ import division

import time
from math import log, sqrt
from random import choice


class Stat(object):
    __slots__ = ('value', 'visits')

    def __init__(self, value=0, visits=0):
        self.value = value
        self.visits = visits


class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        self.board = board
        self.history = []
        self.stats = {}

        self.max_depth = 0
        self.data = {}

        self.calculation_time = float(kwargs.get('time', 30))
        self.max_actions = int(kwargs.get('max_actions', 1000))

        # Exploration constant, increase for more exploratory actions,
        # decrease to prefer actions with known higher win rates.
        self.C = float(kwargs.get('C', 1.4))

    def update(self, state):
        self.history.append(state)

    def display(self, state, action):
        return self.board.display(state, action)

    def winner_message(self, msg):
        return self.board.winner_message(msg)

    def get_action(self):
        # Causes the AI to calculate the best action from the
        # current game state and return it.

        self.max_depth = 0
        self.data = {}

        state = self.history[-1]
        player = self.board.current_player(state)
        legal = self.board.legal_actions(self.history[:])

        # Bail out early if there is no real choice to be made.
        if not legal:
            return
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        # Display the number of calls of `run_simulation` and the
        # time elapsed.
        self.data.update(games=games, max_depth=self.max_depth,
                         time=str(time.time() - begin))
        print self.data['games'], self.data['time']
        print "Maximum depth searched:", self.max_depth

        actions_states = [(p, self.board.next_state(state, p)) for p in legal]

        # Display the stats for each possible action.
        self.data['actions'] = sorted(
            ({'action': p,
              'percent': 100 * self.stats[(player, S)].value / self.stats[(player, S)].visits,
              'wins': self.stats[(player, S)].value,
              'plays': self.stats[(player, S)].visits}
             for p, S in actions_states),
            key=lambda x: (x['percent'], x['plays']),
            reverse=True
        )
        for m in self.data['actions']:
            print "{action}: {percent:.2f}% ({wins} / {plays})".format(**m)

        # Pick the action with the highest percentage of wins.
        percent_wins, num_actions, action = max(
            (self.stats[(player, S)].value / self.stats[(player, S)].visits,
             self.stats[(player, S)].visits,
             p)
            for p, S in actions_states
        )

        return action

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.

        # A bit of an optimization here, so we have a local
        # variable lookup instead of an attribute access each loop.
        stats = self.stats

        visited_states = set()
        history_copy = self.history[:]
        state = history_copy[-1]
        player = self.board.current_player(state)

        expand = True
        for t in xrange(1, self.max_actions + 1):
            legal = self.board.legal_actions(history_copy)
            actions_states = [(p, self.board.next_state(state, p)) for p in legal]

            if all((player, S) in stats for p, S in actions_states):
                # If we have stats on all of the legal actions here, use UCB1.
                log_total = log(
                    sum(stats[(player, S)].visits for p, S in actions_states))
                value, action, state = max(
                    ((stats[(player, S)].value / stats[(player, S)].visits) +
                     self.C * sqrt(log_total / stats[(player, S)].visits), p, S)
                    for p, S in actions_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                action, state = choice(actions_states)

            history_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state) not in stats:
                expand = False
                stats[(player, state)] = Stat()
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, state))

            player = self.board.current_player(state)
            winner = self.board.winner(history_copy)
            if winner:
                break

        for player, state in visited_states:
            if (player, state) not in stats:
                continue
            S = stats[(player, state)]
            S.visits += 1
            if player == winner:
                S.value += 1


class ValueMonteCarlo(object):
    def __init__(self, board, **kwargs):
        self.board = board
        self.history = []
        self.stats = {}

        self.max_depth = 0
        self.data = {}

        self.calculation_time = float(kwargs.get('time', 30))
        self.max_actions = int(kwargs.get('max_actions', 1000))

        # Exploration constant, increase for more exploratory actions,
        # decrease to prefer actions with known higher win rates.
        self.C = float(kwargs.get('C', 1.4))

    def update(self, state):
        self.history.append(state)

    def display(self, state, action):
        return self.board.display(state, action)

    def winner_message(self, msg):
        return self.board.winner_message(msg)

    def get_action(self):
        # Causes the AI to calculate the best action from the
        # current game state and return it.

        self.max_depth = 0
        self.data = {}

        state = self.history[-1]
        player = self.board.current_player(state)
        legal = self.board.legal_actions(self.history[:])

        # Bail out early if there is no real choice to be made.
        if not legal:
            return
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        # Display the number of calls of `run_simulation` and the
        # time elapsed.
        self.data.update(games=games, max_depth=self.max_depth,
                         time=str(time.time() - begin))
        print self.data['games'], self.data['time']
        print "Maximum depth searched:", self.max_depth

        actions_states = [(p, self.board.next_state(state, p)) for p in legal]

        # Display the stats for each possible action.
        self.data['actions'] = sorted(
            ({'action': p,
              'average': self.stats[(player, S)].value / self.stats[(player, S)].visits,
              'sum': self.stats[(player, S)].value,
              'plays': self.stats[(player, S)].visits}
             for p, S in actions_states),
            key=lambda x: (x['average'], x['plays']),
            reverse=True
        )
        for m in self.data['actions']:
            print "{action}: {average:.1f} ({sum} / {plays})".format(**m)

        # Pick the action with the highest average value.
        average, num_actions, action = max(
            (self.stats[(player, S)].value / self.stats[(player, S)].visits,
             self.stats[(player, S)].visits,
             p)
            for p, S in actions_states
        )

        return action

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.

        # A bit of an optimization here, so we have a local
        # variable lookup instead of an attribute access each loop.
        stats = self.stats

        visited_states = set()
        history_copy = self.history[:]
        state = history_copy[-1]
        player = self.board.current_player(state)

        expand = True
        for t in xrange(1, self.max_actions + 1):
            legal = self.board.legal_actions(history_copy)
            actions_states = [(p, self.board.next_state(state, p)) for p in legal]

            if all((player, S) in stats for p, S in actions_states):
                # If we have stats on all of the legal actions here, use UCB1.
                log_total = log(
                    sum(stats[(player, S)].visits for p, S in actions_states))
                value, action, state = max(
                    ((stats[(player, S)].value / stats[(player, S)].visits) +
                     self.C * sqrt(log_total / stats[(player, S)].visits), p, S)
                    for p, S in actions_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                action, state = choice(actions_states)

            history_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state) not in stats:
                expand = False
                stats[(player, state)] = Stat()
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, state))

            player = self.board.current_player(state)
            winner = self.board.winner(history_copy)
            if winner:
                break

        player_values = {}
        for player, state in visited_states:
            if (player, state) not in stats:
                continue
            if player not in player_values:
                player_values[player] = self.board.end_value(history_copy, player)

            S = stats[(player, state)]
            S.visits += 1
            if player_values[player] is not None:
                S.value += player_values[player]
