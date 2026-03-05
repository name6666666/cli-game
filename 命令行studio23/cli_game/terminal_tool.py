import os


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

def get_key(prompt:str=''):
    if os.name == 'nt':
        import msvcrt
        print(prompt, end='')
        return msvcrt.getch().decode('utf-8', errors='ignore')
    else:
        return input(prompt)

__all__ = [
    'run',
    'clean',
    'pause',
    'get_key'
]
