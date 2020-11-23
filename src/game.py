# Imports Selenium
# import os
import time
import io
from selenium import webdrive
from selenium.webdriver.common.keys import Keys, Options
from PIL import Image, ImageFilter
import numpy as np

'''
* class Jogo: Classe que irá representar a interface entre o selenium via python
 e o navegador.
* __init__():  Launch the broswer window using the attributes in chrome_options
* get_crashed() : return true if the agent as crashed on an obstacles. Gets
javascript variable from game decribing the state
* get_playing(): true if game in progress, false is crashed or paused
* restart() : sends a signal to browser-javascript to restart the game
* press_up(): sends a single to press up get to the browser
* press_down(): envia um press down para o browser
* get_score(): gets current game score from javascript variables.
* pause(): pause the game
* resume(): resume a paused game if not crashed
* end(): close the browser and end the game
'''


class Jogo:
    def __init__(self, id, conf_customizada: bool = False):
        # definindo as opções
        chrome_options = Options()
        chrome_options.add_argument("disable-infobars")
        self._driver = webdriver.Firefox(executable_path=r'D:\Arquivos de Programas\geckodriver\geckodriver.exe')
        self._driver.get('https://wayou.github.io/t-rex-runner/')
        self._driver.set_window_position(x=-10+500*(id//3), y=(id%3)*300)
        self._driver.set_window_size(200, 300)

        # modificando o jogo antes de treinar
        if conf_customizada:
            self._driver.execute_script("Runner.config.ACCELERATION=0")

    def get_crashed(self):
        return self._driver.execute_script("return Runner.instance_.crashed")

    def get_playing(self):
        return self._driver.execute_script("return Runner.instance_.playing")
 
    def get_frames(self):
        
        img1 = Image.open(io.BytesIO(self._driver.get_screenshot_as_png()))
        img1 = img1.convert("L")
        img1 = img1.resize((50, 15), Image.BICUBIC, (50, 40, 567, 188))
        img1 = img1.filter(ImageFilter.FIND_EDGES)

        img2 = Image.open(io.BytesIO(self._driver.get_screenshot_as_png()))
        img2 = img2.convert("L")
        img2 = img2.resize((50, 15), Image.BICUBIC, (50, 40, 567, 188))
        img2 = img2.filter(ImageFilter.FIND_EDGES)

        return (img1, img2)

    def restart(self):
        self.pause()
        self._driver.execute_script("Runner.instance_.restart()")
        
    def jump(self):
        self._driver.find_element_by_tag_name("body").send_keys(Keys.SPACE)
        
    def duck(self):
        self._driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_DOWN)
        
    def get_score(self):
        score_array = self._driver.execute_script(
            "return Runner.instance_.distanceMeter.digits")
        # the javascript object is of type array with score in the
        #   formate[1,0,0] which is 100.
        score = ''.join(score_array)
        return int(score)

    def pause(self):
        return self._driver.execute_script("return Runner.instance_.stop()")

    def resume(self):
        return self._driver.execute_script("return Runner.instance_.play()")

    def end(self):
        self._driver.close()


class Agent:
    def __init__(self,game):
        self._game = game
        self.alive = True
    def doAction(self,actions):
        self._game.resume()
        if actions[2] == 1:
            self._game.duck()
        elif actions[1] == 1: #else do nothing
            self._game.jump()
        self._game.pause()
    def update(self):
        if self.alive:
            self._game.resume()
            if self._game.get_crashed():    
                self.alive = False
            
            frames = self._game.get_frames()
            self._game.pause()
            return frames
        else:
            return None
    def reset(self):
        self.alive = True
        self._game.restart()
    def getFinalScore(self):
        return self._game.get_score()

a = Jogo(0)
b = Jogo(1)
c = Jogo(2)
d = Jogo(3)
e = Jogo(4)
f = Jogo(5)
'''
input("awaiting input")
a.pause()
a.resume()
t=a.get_frames()
t[0].save('teste1.png')
t[1].save('teste2.png')
a.pause()
'''
