from abc import ABC, abstractmethod
from . import Component
from ..string_tool import Border, add_border



class Item(ABC):
    @abstractmethod
    def update(self, input):
        pass

    @abstractmethod
    def __str__(self):
        pass


class List(Component):
    def __init__(self, *args, border:Border=None, title=''):
        super().__init__()
        self.title = title
        self.list:list[Item|str] = list(args)
        self.border = border

    @staticmethod
    def line_beginning(index):
        return f'{index + 1}. '

    def get_string(self) -> str:
        result = (f'{self.title}\n' if self.title else '') + '\n'.join(self.line_beginning(i) + str(self.list[i]) for i in range(len(self.list)))
        return add_border(result, self.border) if self.border is not None else result

    def update(self, input):
        for i in self.list.copy():
            if isinstance(i, Item):
                i.update(input)

__all__ = [
    'Item',
    'List'
]
