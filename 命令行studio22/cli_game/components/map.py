from typing import final, Literal, Any
from copy import copy, deepcopy
from abc import ABC, abstractmethod
from ..exception import CharWidthError, ClassNameError
from . import Component
from ..string_tool import Border, add_border, get_width


class Char(ABC):
    subclasses = {}


    @final
    def __init_subclass__(cls, *, name: str = None, **kwargs):
        name = cls.__name__ if name is None else name
        if name in Char.subclasses:
            raise ClassNameError(f'Duplicated class name {name}')
        Char.subclasses[name] = cls

    def __init__(self, row: int = None, column: int = None, map: Map = None):
        self._row = row
        self._column = column
        self.map = map

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

    def find(self, pos: tuple[int, int] | Literal['w', 'a', 's', 'd']) -> Char | None:
        target = ...
        match pos:
            case 'w':
                target = (-1, 0)
            case 's':
                target = (1, 0)
            case 'a':
                target = (0, -1)
            case 'd':
                target = (0, 1)
            case (x, y):
                target = (x, y)
        target = (self._row + target[0], self._column + target[1])
        if (target[0] < 0) or (target[1] < 0):
            return None
        try:
            return self.map.list[target[0]][target[1]]
        except IndexError:
            return None

    def change_to(self, new_char: Char, pos=(0, 0), deep_copy=False) -> bool:
        if new_char is self:
            new_char = deepcopy(new_char) if deep_copy else copy(new_char)
        new_char._row = self._row + pos[0]
        new_char._column = self._column + pos[1]
        new_char.map = self.map
        try:
            if (new_char._row < 0) or (new_char._column < 0): raise IndexError
            self.map.list[new_char._row][new_char._column] = new_char
            return True
        except IndexError:
            return False

    def move(self, directory: Literal['w', 'a', 's', 'd'] | Any, leave: type = None, accessible: set | list | tuple = None) -> bool | None:
        pos = ...
        match directory:
            case 'w':
                pos = (-1, 0)
            case 's':
                pos = (1, 0)
            case 'a':
                pos = (0, -1)
            case 'd':
                pos = (0, 1)
            case _:
                return None
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
        self.map.list[self._row][self._column] = (Char.subclasses['Void'] if leave is None else leave)(self._row,
                                                                                                       self._column,
                                                                                                       self.map)
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


class Map(Component):
    def __init__(self, content: str | list[list[Char]], *, char_width=3, border:Border=None):
        super().__init__()
        self.char_width = char_width
        self.border = border
        if isinstance(content, str):
            lines = content.splitlines()
            map_list = [i.split() for i in lines if i.strip()]
            map_list = [[Char.subclasses[map_list[i][j]](i, j, self) for j in range(len(map_list[i]))] for i in
                        range(len(map_list))]
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
                if get_width(string) > self.char_width:
                    raise CharWidthError(f'Width of "{string}" is {get_width(string)}, bigger than {self.char_width}.')
                string = string + (self.char_width - get_width(string)) * ' '
                result += string
            result += '\n'
        return add_border(result, self.border) if self.border is not None else result

    def update(self, input):
        for i in [i.copy() for i in self.list]:
            for j in i:
                j.update(input)



__all__ = [
    'Char',
    'Void',
    'Map'
]
