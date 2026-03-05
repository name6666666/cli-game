from cli_game.components import *
from cli_game.components.map import *
from cli_game.terminal_tool import *
from cli_game.components.list import *
from cli_game.string_tool import *
from cli_game.components.debugger import *
from cli_game.storage import *
import random as r

run()

class MyStorage(Storage):
    __target_path__ = 'G:/python项目/命令行studio/save.json'
    manager = ComponentsManager()


row = 0
column = 0
class Me(Char):
    def char(self) -> str:
        return c**'${Fblue}我'
    def update(self, input):
        self.move(input)
        global row, column
        row = self.row
        column = self.column
class Monster(Char, name='M'):
    def char(self) -> str:
        return c**'${Fred}怪'
    def update(self, input):
        delta = (row - self.row, column - self.column)
        if delta[0] > 0:
            result = self.move('s')
        else:
            result = self.move('w')
        if not result:
            if delta[1] > 0:
                result = self.move('d')
            else:
                result = self.move('a')
        if not result:
            self.move(r.randint(0, 3))
class Tree(Char, name='T'):
    def char(self) -> str:
        return c**'${Fgreen}树'
    def update(self, input):
        pass

border = Border('''
* - *
|   |
* - *
''', style='Fyellow')

map = Map('''
T T T T T  T T
T V V V Me T T
V T V V V  V V
V V V T V  T T
T T T V V  V T
T M V V V  V T
'''.replace('V', 'Void'), border=border)

MyStorage.manager.registry_group('1', [debugger, map])
MyStorage.manager.activated_group = '1'


try:
    MyStorage.load()
except FileNotFoundError:
    MyStorage.dump()

try:
    while True:
        MyStorage.manager.refresh(get_key, '> ')
        MyStorage.dump()
except:
    import traceback
    traceback.print_exc()
    pause()
