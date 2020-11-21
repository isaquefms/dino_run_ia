import time


class DinoAgent:

    # takes game as input for taking actions
    def __init__(self, game):
        self._game = game
        self.jump()  # to start the game, we need to jump once
        # no action can be performed for the first time when game starts
        time.sleep(.5)

    def is_running(self):
        return self._game.get_playing()

    def is_crashed(self):
        return self._game.get_crashed()

    def jump(self):
        self._game.press_up()

    def duck(self):
        self._game.press_down()
