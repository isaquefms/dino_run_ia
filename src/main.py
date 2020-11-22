from game import Jogo
from model import buildmodel
from agent import DinoAgent
from training import train_network
from game_state import GameState


def play_game():
    game = Jogo()
    dino = DinoAgent(game)
    game_state = GameState(dino, game)
    model = buildmodel()
    try:
        train_network(model, game_state)
    except StopIteration:
        game.end()


play_game()
