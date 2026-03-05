from cli_game.components import *
from cli_game.components.map import *
from cli_game.terminal_tool import *
from cli_game.components.list import *
from cli_game.string_tool import *
from cli_game.components.debugger import *
from cli_game.storage import *
import random as r

run(exit=False)




class Me(Char):
    def update(self, input):
        self.move(input)

    def char(self) -> str:
        return c**'${Fred}我'

class Tree(Char, name='T'):
    def update(self, input):
        pass

    def char(self) -> str:
        return '树'

class Monster(Char, name='M'):
    def update(self, input):
        directory = ...
        match r.randint(0, 3):
            case 0:
                directory = 'w'
            case 1:
                directory = 'a'
            case 2:
                directory = 's'
            case 3:
                directory = 'd'
        self.move(directory)


    def char(self) -> str:
        return '怪'

def init():
    border = Border('''
    _ _ _
    |   |
    * - *
    ''', min_width=20, style='Fred')

    lst = List('fuck', 'asshole', 'pussy', title='polite words', border=border)


    m = Map('''
    T T T T T T
    T T T T V T
    T Me V V V T
    T V T V T T
    T V V V M T
    T T T T T T
    '''.replace('V', 'Void'), border=border)

    debugger.accumulate = False
    g = Group(debugger, m, lst)
    g.activate()

    return g
class Test(Storage):
    __target_path__ = 'G:\python项目\命令行studio\save.json'
    group:Group = init()
Test.load()
print(Test.group)

try:
    while True:
        Test.group.refresh(get_key, '> ')
        Test.dump()
except Exception:
    import traceback
    traceback.print_exc()
    pause()
