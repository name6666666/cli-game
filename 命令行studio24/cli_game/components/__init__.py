from abc import ABC, abstractmethod
from typing import final, Callable
from ..exception import ClassNameError
from ..terminal_tool import clean



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

class Group:
    _activated:Group = None

    def __init__(self, *args:Component):
        self.components = args

    def activate(self):
        Group._activated = self

    @staticmethod
    def refresh(input_func:Callable, prompt:str):
        string = ''
        for i in Group._activated.components:
            string += i.get_string()
        clean()
        print(string, flush=True)
        input_content = input_func(prompt)
        for i in Group._activated.components:
            i.update(input_content)



__all__ = [
    'Component',
    'Group'
]
