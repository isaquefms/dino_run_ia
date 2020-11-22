class GameState:

    def __init__(self, agent, game):
        self._agent = agent
        self._game = game

    def get_state(self, actions):
        score = self._game.get_score()
        reward = 0.1*score/10  # dynamic reward calculation
        is_over = False  # game over
        if actions[1] == 1:  # else do nothing
            self._agent.jump()
            reward = 0.1*score/11
        # Todo: Declarar essa e as demais funções do open_cv
        image = ''  # grab_screen()

        if self._agent.is_crashed():
            self._game.restart()
            reward = -11/score
            is_over = True
        return image, reward, is_over  # return the Experience tuple


'''
get_state(): accepts an array of actions,
             performs the action on the agent
returns :  new state, reward and if the game ended.
'''


# class Game_sate:
#     def __init__(self,agent,game):
#         self._agent = agent
#         self._game = game
#     def get_state(self,actions):
#         score = self._game.get_score()
#         reward = 0.1*score/10 # dynamic reward calculation
#         is_over = False #game over
#         if actions[1] == 1: #else do nothing
#             self._agent.jump()
#             reward = 0.1*score/11
#         image = grab_screen()
#
#         if self._agent.is_crashed():
#             self._game.restart()
#             reward = -11/score
#             is_over = True
#         return image, reward, is_over #return the Experience tuple
