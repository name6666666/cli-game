from . import Component
from ..string_tool import get_width


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
        print()
        while (inp := input('求值或执行语句: ')) != 'end':
            try:
                print(eval(inp, globals=glo, locals=loc))
            except:
                try:
                    exec(inp, globals=glo, locals=loc)
                    print('执行成功。')
                except:
                    import traceback
                    traceback.print_exc()

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