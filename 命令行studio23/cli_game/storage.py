from pathlib import Path
import json


class Storage:
    path: str | Path = ''
    prefix = 'st'

    @staticmethod
    def dump(globals: dict, path: str | Path=None):
        path = path if path is not None else Storage.path
        target = {k : v for k, v in globals.items() if k.startswith(f'{Storage.prefix}_') or k.startswith(f'_{Storage.prefix}_')}
        with open(str(path), 'w') as f:
            json.dump(target, f, indent=4)

    @staticmethod
    def load(globals: dict, path: str | Path=None):
        path = path if path is not None else Storage.path
        if not Path(path).is_file():
            return
        with open(str(path), 'r') as f:
            result = json.load(f)
        for k, v in result.items():
            if k in globals:
                globals[k] = v


__all__ = [
    'Storage'
]
