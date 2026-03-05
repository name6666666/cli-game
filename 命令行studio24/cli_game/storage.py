from pathlib import Path
from abc import ABC
import jsonpickle


class Storage(ABC):
    __target_path__: str | Path = ''

    @classmethod
    def _get_attr(cls):
        return {k: v for k, v in cls.__dict__.items() if not (k.startswith('__') and k.endswith('__'))}

    @classmethod
    def _set_attr(cls, dct:dict):
        for k, v in dct.items():
            if k in cls.__dict__:
                setattr(cls, k, v)

    @classmethod
    def dumps(cls):
        return jsonpickle.dumps(cls._get_attr(), indent=4)

    @classmethod
    def dump(cls, path: str | Path=None):
        path = cls.__target_path__ if path is None else path
        with open(str(path), 'w') as f:
            f.write(cls.dumps())

    @classmethod
    def loads(cls, json_string):
        cls._set_attr(jsonpickle.loads(json_string))

    @classmethod
    def load(cls, path: str | Path=None):
        path = cls.__target_path__ if path is None else path
        with open(str(path), 'r') as f:
            cls.loads(f.read())


__all__ = [
    'Storage'
]

