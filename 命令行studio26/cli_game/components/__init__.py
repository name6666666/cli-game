from abc import ABC, abstractmethod
from typing import final, Callable
from ..exception import ClassNameError, GroupError
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

class ComponentsManager:

    def __init__(self):
        self._group = {}
        self._activated = None

    def registry_group(self, name:str, components:list[Component]):
        if name in self._group:
            raise GroupError(f'Duplicated group name {name}.')
        self._group[name] = components

    @property
    def activated_group(self):
        return self._activated
    @activated_group.setter
    def activated_group(self, name:str):
        if name not in self._group:
            raise GroupError(f'Group {name} dose not exist.')
        if not isinstance(name, str):
            raise TypeError(f'Invalid type {type(name).__name__}')
        self._activated = name

    def refresh(self, input_func:Callable, prompt:str):
        if self._activated is None:
            raise GroupError('No group activated.')
        string = ''
        for i in self._group[self._activated]:
            string += i.get_string()
        clean()
        print(string, flush=True)
        input_content = input_func(prompt)
        for i in self._group[self._activated]:
            i.update(input_content)



__all__ = [
    'Component',
    'ComponentsManager'
]
