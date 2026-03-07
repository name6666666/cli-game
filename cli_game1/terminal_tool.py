import os
from typing import Callable


def run(exit=True):
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
        if exit: sys.exit(0)


def clean():
    if os.name == 'nt':
        os.system('cls')

def pause():
    os.system('pause')

def get_key(prompt:str='', wait='/'):
    if os.name == 'nt':
        import msvcrt
        print(prompt, end='', flush=True)
        result = msvcrt.getch().decode('utf-8', errors='ignore')
        if result and (result in wait):
            return result + input(result)
        return result
    else:
        return input(prompt)

def mainloop(func:Callable):
    try:
        while True:
            func()
    except SystemExit:
        pause()
    except:
        import traceback
        from colorama import Fore
        print(Fore.RED, end='')
        traceback.print_exc()
        print(Fore.RESET, end='')
        pause()


__all__ = [
    'run',
    'clean',
    'pause',
    'get_key',
    'mainloop'
]
