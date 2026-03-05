from . import Component
from ..string_tool import get_width
from colorama import Fore


def _debug_loop(glo, loc):
    print()
    while (inp := input('求值或执行语句: ')) != '/end':
        if inp == '/clean':
            from ..terminal_tool import clean
            clean()
            continue
        try:
            print(eval(inp, globals=glo, locals=loc))
        except SyntaxError:
            try:
                exec(inp, globals=glo, locals=loc)
                print('执行成功。')
            except:
                import traceback
                print(Fore.RED, end='')
                traceback.print_exc()
                print(Fore.RESET, end='')
        except:
            import traceback
            print(Fore.RED, end='')
            traceback.print_exc()
            print(Fore.RESET, end='')

class _Debugger(Component):
    def __init__(self):
        super().__init__()
        self._output = ''
        self.title = 'debug'
        self.accumulate = True

    def update(self, input):
        if self.accumulate:
            self._output += f'\ninput: {input}\n'
        else:
            self._output = f'input: {input}\n'
        if input == '/debug':
            import sys
            glo = sys.modules['__main__'].__dict__
            _debug_loop(glo, {})


    def output(self, *args, end='\n', separate=' '):
        self._output += separate.join(str(i) for i in args) + end

    @staticmethod
    def break_point():
        import inspect
        frame = inspect.currentframe().f_back
        try:
            glo = frame.f_globals
            loc = frame.f_locals
        finally:
            del frame
        _debug_loop(glo, loc)


    def __lshift__(self, other):
        self._output += str(other) + '\n'
        return self

    def get_string(self):
        result = ''
        result += f'====={self.title}=====\n'
        result += self._output
        result += f'\n====={get_width(self.title) * '='}=====\n'
        return result

debugger = _Debugger()


__all__ = [
    'debugger'
]
