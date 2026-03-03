from cli_game import *
import random as r

run()

class Me(Char):
    def update(self, input):
        match input:
            case 'w':
                self.move('u')
            case 's':
                self.move('d')
            case 'a':
                self.move('l')
            case 'd':
                self.move('r')

    def char(self) -> str:
        return '我'

class Tree(Char, name='T'):
    def update(self, input):
        pass

    def char(self) -> str:
        return '树'

class Monster(Char, name='M'):
    def update(self, input):
        a = ...
        match r.randint(0, 3):
            case 0:
                a = self.move('l')
            case 1:
                a = self.move('r')
            case 2:
                a = self.move('d')
            case 3:
                a = self.move('u')
        self.out << ('通行成功' if a else '通行失败')

    def char(self) -> str:
        return '怪'


m = Map('''
T T T T T T
T T T T V T
T Me V V V T
T V T V T T
T V V V M T
T T T T T T
'''.replace('V', 'Void'))

out.accumulate = False
g = Group(out, m)
g.activated()
while True:
    g.refresh(get_key, '>')
pause()
