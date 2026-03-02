import sys
import os

if os.name != 'nt':
    print('Invalid platform. Windows only.')
    sys.exit(1)

if len(sys.argv) == 1:
    from tempfile import TemporaryFile
    from pathlib import Path
    import time

    file = Path(__file__)

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
    sys.exit(0)



from cli_game import Char, Map, update, get_key, out, clean, pause


class Me(Char):
    def update(self, input):
        match input:
            case 'w':
                out << self.move('u')
            case 's':
                out << self.move('d')
            case 'a':
                out << self.move('l')
            case 'd':
                out << self.move('r')

    def char(self) -> str:
        return '我'

class Tree(Char):
    def update(self, input):
        pass

    def char(self) -> str:
        return '树'


m = Map('''
Tree Tree Tree
Me Void Void
Void Tree Void
Void Void Void
''')


while True:
    clean()
    out.print()
    m.print()
    update(get_key('>'))
pause()
