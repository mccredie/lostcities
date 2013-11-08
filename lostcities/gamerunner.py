
import abc

from . import playgameproxy
from . import drawgameproxy


class Player(metaclass=abc.ABCMeta):
    """ This class represents the interface that must be implemented to
    interface with the game via a game runner. It could be implemented to
    interact with a user interface to get the game decisions from the player.
    It could also be implemented as an AI. 
    """

    @abc.abstractmethod
    def play_card(self, play_proxy):
        """ When called by the runner, the implementation must use the proxy
        parameter to either 'play' or 'discard' a card.
        """
        pass


    @abc.abstractmethod
    def draw(self, draw_proxy):
        """ When called by the runner, the implementation must use the proxy
        parameter to either 'draw' or 'draw_from' a card.
        """
        pass


    def they_drew(self):
        """ Called when the other play performs the 'draw' action. """
        pass


    def they_drew_from(self, card):
        """ Called when the other play performs the 'draw_from' action. The
        'card' parameter is the value of the card that was drawn.
        """
        pass


    def they_discarded(self, card):
        """ Called when the other play performs the 'discard' action. The
        'card' parameter is the value of the card that was discarded.
        """
        pass


    def they_played(self, card):
        """ Called when the other play performs the 'play' action. The
        'card' parameter is the value of the card that was played.
        """
        pass



class _GameRunnerState:
    def __init__(self, do, *args):
        self.next_state = self
        self.current_player = None
        self.other_player = None
        self._do = do
        self._args = args


    def update(self):
        self._do(*self._args)



def _get_init_state(p1, p2, runner, game):
    p1_play_proxy = playgameproxy.PlayGameProxy(game, runner, 0)
    p1_draw_proxy = drawgameproxy.DrawGameProxy(game, runner, 0)
    p2_play_proxy = playgameproxy.PlayGameProxy(game, runner, 1)
    p2_draw_proxy = drawgameproxy.DrawGameProxy(game, runner, 1)

    p1_play_card = _GameRunnerState(p1.play_card, p1_play_proxy)
    p1_play_card.current_player = p1
    p1_play_card.other_player = p2

    p1_draw = _GameRunnerState(p1.draw, p1_draw_proxy)
    p1_draw.current_player = p1
    p1_draw.other_player = p2

    p2_play_card = _GameRunnerState(p2.play_card, p2_play_proxy)
    p2_play_card.current_player = p2
    p2_play_card.other_player = p1

    p2_draw = _GameRunnerState(p2.draw, p2_draw_proxy)
    p2_draw.current_player = p2
    p2_draw.other_player = p1

    p1_play_card.next_state = p1_draw
    p1_draw.next_state = p2_play_card
    p2_play_card.next_state = p2_draw
    p2_draw.next_state = p1_play_card
    return p1_play_card



class GameRunner(object):
    def __init__(self, game, p1, p2):
        self._state = _get_init_state(p1, p2, self, game)
        self._game = game
        self.game_is_over = game.game_over


    def update(self):
        self._state.update()
        self.game_is_over = self._game.game_over


    def finish_play(self, card):
        self._state.other_player.they_played(card)
        self._state = self._state.next_state


    def finish_discard(self, card):
        self._state.other_player.they_discarded(card)
        self._state = self._state.next_state


    def finish_draw(self):
        self._state.other_player.they_drew()
        self._state = self._state.next_state


    def finish_draw_from(self, card):
        self._state.other_player.they_drew_from(card)
        self._state = self._state.next_state




