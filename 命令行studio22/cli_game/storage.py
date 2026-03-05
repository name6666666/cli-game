from typing import final
from pathlib import Path
import json



class Storage:
    _objs = {}
    path: Path | str = ''

    @staticmethod
    def dump():
        with open(str(Storage.path), 'w', encoding='utf-8') as f:
            json.dump(Storage._objs, f, indent=4)

    @final
    def __init_subclass__(cls, **kwargs):

        def __new__(cls_, value, name: str):
            if Path(Storage.path).is_file():
                with open(str(Storage.path), 'r', encoding='utf-8') as f:
                    value = json.load(f)[name]
            obj = cls_.__bases__[0].__new__(cls_, value)
            Storage._objs[name] = obj
            obj.name = name
            return obj

        cls.__new__ = __new__


class Int(int, Storage):
    def __new__(cls, value, name: str) -> int:
        ...

class Float(float, Storage):
    def __new__(cls, value, name:str) -> float:
        ...

class Str(str, Storage):
    def __new__(cls, value, name:str) -> str:
        ...



Storage.path = r'G:\python项目\命令行studio\save.sav'

a = Int(5, 'a')

Storage.dump()