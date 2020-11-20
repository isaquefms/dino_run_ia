# Imports Selenium
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Jogo:
    """Classe que irá representar a interface entre o selenium via python e o
    navegador.
    """

    def __init__(self, conf_customizada: bool = True):
        # definindo as opções
        chrome_options = Options()
        chrome_options.add_argument("disable-infobars")
        self._driver = webdriver.Chrome(executable_path='',
                                        chrome_options=chrome_options)
        self._driver.set_window_position(x=-10, y=0)
        self._driver.set_window_size(200, 300)
        self._driver.get(os.path.abspath(''))
        # modificando o jogo antes de treinar
        if conf_customizada:
            self._driver.execute_script("Runner.config.ACCELERATION=0")
