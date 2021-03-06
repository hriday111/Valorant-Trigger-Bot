__author__: str = 'hday'
__version__: str = 'v2.0.0'
from keyboard import is_pressed
from os import system
from time import perf_counter, sleep
from ctypes import windll
from PIL import ImageGrab, Image
from winsound import Beep 
from mss import mss
from colorama import Fore, Style, init
run=False
S_HEIGHT, S_WIDTH = (ImageGrab.grab().size)
GRABZONE: int = 10
TRIGGER_KEY: str = 'shift'
SWITCH_KEY: str = 'ctrl + tab'
GRABZONE_KEY_UP: str = 'ctrl + up'
GRABZONE_KEY_DOWN: str = 'ctrl + down'
mods: tuple = ('0.3s Delay', '0.2s Delay', '0.1s Delay', 'No Delay Full-Auto')
 
class FoundEnemy(Exception):
    pass
 
class TriggerBot:
    def __init__(self) -> None:
        self._mode: int = 2
        self._last_reac: int = 0
        
    def switch(self):
        if self._mode != 3: self._mode += 1
        else: self._mode = 0

        if self._mode == 0: Beep(200, 100)
        elif self._mode == 1: Beep(200, 100), Beep(200, 100)
        elif self._mode == 2: Beep(200, 100), Beep(200, 100), Beep(200, 100)
        elif self._mode == 3: Beep(200, 100), Beep(200, 100), Beep(200, 100), Beep(200, 100)
 
    def color_check(self, red: int, green: int, blue: int) -> bool:
        if green >= 190:
            return False
        
        if green >= 140:
            return abs(red - blue) <= 8 and red - green >= 50 and blue - green >= 50 and red >= 105 and blue >= 105

        return abs(red - blue) <= 13 and red - green >= 60 and blue - green >= 60 and red >= 110 and blue >= 100

    def grab(self) -> Image:
        with mss() as sct:
            bbox: tuple = (int(S_HEIGHT / 2 - GRABZONE), int(S_WIDTH / 2 - GRABZONE), int(S_HEIGHT / 2 + GRABZONE), int(S_WIDTH / 2 + GRABZONE))
            sct_img = sct.grab(bbox)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    
    def scan(self) -> None:
        start_time: float = perf_counter()
        pmap: Image = self.grab()
        
        try:
            for x in range(0, GRABZONE*2):
                for y in range(0, GRABZONE*2):
                    r, g, b = pmap.getpixel((x,y))
                    if self.color_check(r, g, b): raise FoundEnemy

        except FoundEnemy:
            self._last_reac = int((perf_counter() - start_time)*1000)

            windll.user32.mouse_event(2, 0, 0, 0, 0)
            windll.user32.mouse_event(4, 0, 0, 0, 0)

            if self._mode == 0: sleep(0.3)
            elif self._mode == 1: sleep(0.2)
            elif self._mode == 2: sleep(0.1)
            elif self._mode == 3: pass

def print_banner(bot: TriggerBot) -> None:
    system('cls')
    print(Style.BRIGHT + Fore.CYAN + f'{__author__} Valorant External Cheat {__version__}' + Style.RESET_ALL)
    print('====== Controls ======')
    print('Trigger Key          :', Fore.YELLOW + TRIGGER_KEY + Style.RESET_ALL)
    print('Mode Chage Key       :', Fore.YELLOW + SWITCH_KEY + Style.RESET_ALL)
    print('Grab Zone Change Key :', Fore.YELLOW + GRABZONE_KEY_UP + '/' + GRABZONE_KEY_DOWN + Style.RESET_ALL)
    print('===== Information ====')
    print('Mode                 :', Fore.CYAN + mods[bot._mode] + Style.RESET_ALL)
    print('Grab Zone            :', Fore.CYAN + str(GRABZONE) + 'x' + str(GRABZONE) + Style.RESET_ALL)
    print('Trigger Status       :', Fore.GREEN + f'Hold down the "{TRIGGER_KEY}" key' + Style.RESET_ALL)
    print('Last React Time      :', Fore.CYAN + str(bot._last_reac) + Style.RESET_ALL + ' ms (' + str((bot._last_reac)/(GRABZONE*GRABZONE)) + 'ms/pix)')

if __name__ == "__main__":
    print('e340d4e42d032023127fcd4a42ea34349fc0b00b982047ad614d405fc2cd1168')
    init()
    system('@echo off')
    system('cls')
    bot = TriggerBot()
    print_banner(bot)

    while True:
        if is_pressed(SWITCH_KEY):
            bot.switch()
            print_banner(bot)

        if is_pressed(GRABZONE_KEY_UP):
            GRABZONE += 1
            print_banner(bot)
            Beep(400, 100)

        if is_pressed(GRABZONE_KEY_DOWN):
            if GRABZONE != 1: GRABZONE -= 1
            print_banner(bot)
            Beep(300, 100)

        if is_pressed('alt'):
            bot.scan()
            print_banner(bot)