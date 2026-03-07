from math import floor
from . import Component
from ..string_tool import colored_string


class ProgressBar(Component):
    def __init__(self, right:int|float, *, text:str='', left:int|float=0, color:str='green', width:int=None):
        super().__init__()
        self.text = text
        self._left = left
        self.right = right
        self.color = color
        self.width = self.right if width is None else width

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = min(max(0, value), self.right)

    def get_string(self) -> str:
        result = self.text + (filled := floor(self._left / self.right * self.width)) * colored_string(f'$[B{self.color}] ') + (self.width - filled) * '-' + f' {self._left:g}/{self.right:g}'
        return result + '\n'

    def update(self, input):
        pass

__all__ = [
    'ProgressBar'
]
