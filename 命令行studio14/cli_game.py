from wcwidth import wcswidth
from abc import ABC, abstractmethod
from typing import final, Literal, Callable
from copy import copy, deepcopy
import msvcrt
import os



def run():
    import sys
    if os.name != 'nt':
        sys.exit(1)
    if len(sys.argv) == 1:
        from tempfile import TemporaryFile
        from pathlib import Path
        import time

        file = Path(sys.argv[0])

        f = TemporaryFile('w', suffix='.bat', delete=False)
        with f:
            f.write(f'''
        {file.drive}
        cd "{file.parent}"
        python "{file.name}" start
        ''')

        try:
            os.startfile(f.name)
            time.sleep(1)
        finally:
            os.unlink(f.name)
        sys.exit(0)


def clean():
    if os.name == 'nt':
        os.system('cls')

def pause():
    os.system('pause')

def get_key(prompt:str=''):
    if os.name == 'nt':
        print(prompt, end='')
        return msvcrt.getch().decode('utf-8', errors='ignore')
    else:
        return input(prompt)

def embed(src_str:str, embed_str:str, side:Literal['l', 'r', 'r_against_l']= 'r_against_l'):
    string_lines = src_str.splitlines()
    embed_lines = embed_str.splitlines()
    string_width = max(wcswidth(i) for i in string_lines)
    embed_width = max(wcswidth(i) for i in embed_lines)
    height = max(len(embed_lines), len(string_lines))
    for _ in range(max(height - len(string_lines), 0)): string_lines.append('')
    for _ in range(max(height - len(embed_lines), 0)): embed_lines.append('')
    result = []
    match side:
        case 'l':
            embed_lines = [i + (embed_width - wcswidth(i)) * ' ' for i in embed_lines]
            result = [i + j for i, j in zip(embed_lines, string_lines)]
        case 'r':
            string_lines = [i + (string_width - wcswidth(i)) * ' ' for i in string_lines]
            result = [i + j for i, j in zip(string_lines, embed_lines)]
        case 'r_against_l':
            string_lines = [i + (string_width - wcswidth(i)) * ' ' for i in string_lines]
            result = [i + j if i.strip() else j for i, j in zip(string_lines, embed_lines)]
        case val:
            raise ValueError(f'Invalid value {val}')
    result = '\n'.join(result)
    return result

class ClassNameError(Exception):
    pass

class Component(ABC):
    subclasses = {}

    @final
    def __init_subclass__(cls, **kwargs):
        cls.objs = []
        if cls.__name__ in Component.subclasses:
            raise ClassNameError(f'Duplicated class name {cls.__name__}')
        Component.subclasses[cls.__name__] = cls

    def __init__(self):
        self.__class__.objs.append(self)

    @abstractmethod
    def update(self, input):
        pass

    @abstractmethod
    def get_string(self) -> str:
        pass

    def print(self):
        print(self.get_string())

def update(input):
    for i in Component.subclasses.values():
        for j in i.objs:
            j.update(input)

class Group:
    _activated:Group = None

    def __init__(self, *args:Component):
        self.components = args

    def activated(self):
        Group._activated = self

    @staticmethod
    def refresh(input:Callable, prompt:str):
        string = ''
        for i in Group._activated.components:
            string += i.get_string()
        clean()
        print(string, flush=True)
        input_content = input(prompt)
        for i in Group._activated.components:
            i.update(input_content)

class _Out(Component):
    def __init__(self):
        super().__init__()
        self._output = ''
        self.title = 'debug'
        self.accumulate = True
        self.end = '\n'

    def update(self, input):
        if self.accumulate:
            self._output += f'\ninput: {input}\n'
        else:
            self._output = f'input: {input}\n'

    def __call__(self, *args, end='\n', separate=' '):
        self._output += separate.join(str(i) for i in args) + end

    def __lshift__(self, other):
        self._output += str(other) + self.end
        return self

    def get_string(self):
        result = ''
        result += f'====={self.title}=====\n'
        result += self._output
        result += f'\n====={wcswidth(self.title) * '='}=====\n'
        return result
out = _Out()


class Char(ABC):
    subclasses = {}

    class _Out:
        def __init__(self, obj:Char):
            self.obj = obj
        def __call__(self, *args, end='\n', separate=' '):
            out(f'{self.obj}:\n', *args, end=end, separate=separate)
        def __lshift__(self, other):
            return out << f'{self.obj}:' << other

    @final
    def __init_subclass__(cls, *, name:str=None, **kwargs):
        name = cls.__name__ if name is None else name
        if name in Char.subclasses:
            raise ClassNameError(f'Duplicated class name {name}')
        Char.subclasses[name] = cls

    def __init__(self, row:int=None, column:int=None, map:Map=None):
        self._row = row
        self._column = column
        self.map = map
        self.out = Char._Out(self)

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def __str__(self):
        return f'{self.char()}({self._row}, {self._column})'

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def char(self) -> str:
        pass

    def change(self, new_char:Char, pos=(0, 0), deep_copy=False):
        if new_char is self:
            new_char = deepcopy(new_char) if deep_copy else copy(new_char)
        new_char._row = self._row + pos[0]
        new_char._column = self._column + pos[1]
        new_char.map = self.map
        self.map.list[self._row + pos[0]][self._column + pos[1]] = new_char

    def move(self, directory:Literal['u', 'd', 'l', 'r'], leave:type=None, accessible:set|list|tuple=None):
        pos = ...
        match directory:
            case 'u':
                pos = (-1, 0)
            case 'd':
                pos = (1, 0)
            case 'l':
                pos = (0, -1)
            case 'r':
                pos = (0, 1)
            case val:
                raise ValueError(f'Invalid Value {val}.')
        try:
            if self._row + pos[0] < 0 or self._column + pos[1] < 0:
                raise IndexError
            target_pos = self.map.list[self._row + pos[0]][self._column + pos[1]]
            if accessible is None:
                if not isinstance(target_pos, Void):
                    return False
            else:
                if type(target_pos) not in accessible:
                    return False
        except IndexError:
            return False
        self.map.list[self._row][self._column] = (Char.subclasses['Void'] if leave is None else leave)(self._row, self._column, self.map)
        self._row += pos[0]
        self._column += pos[1]
        self.map.list[self._row][self._column] = self
        return True
    
    @abstractmethod
    def update(self, input):
        pass

class Void(Char):
    def char(self) -> str:
        return ''

    def update(self, input):
        pass

class CharWidthError(Exception):
    pass

class Map(Component):
    def __init__(self, content: str | list[list[Char]], char_width=3):
        super().__init__()
        self.char_width = char_width
        if isinstance(content, str):
            lines = content.splitlines()
            map_list = [i.split() for i in lines if i.strip()]
            map_list = [[Char.subclasses[map_list[i][j]](i, j, self) for j in range(len(map_list[i]))] for i in range(len(map_list))]
            self.list = map_list
        elif isinstance(content, list):
            self.list = content
        else:
            raise TypeError(f'Unexpected type {type(content).__name__}.')

    def get_string(self):
        result = ''
        for i in self.list:
            for j in i:
                string = j.char()
                if wcswidth(string) > self.char_width:
                    raise CharWidthError(f'Width of "{string}" is {wcswidth(string)}, bigger than {self.char_width}.')
                string = string + (self.char_width - wcswidth(string)) * ' '
                result += string
            result += '\n'
        return result
    
    def update(self, input):
        for i in [i.copy() for i in self.list]:
            for j in i:
                j.update(input)

__all__ = [
    'Map',
    'Void',
    'Char',
    'update',
    'Component',
    'get_key',
    'clean',
    'out',
    'pause',
    'run',
    'embed',
    'Group'
]
