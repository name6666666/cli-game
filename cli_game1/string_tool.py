from string import Template
from typing import Literal
from colorama import Fore, Style, Back
from rich.text import Text
from .exception import BorderError, CharWidthError



class BetterTemplate(Template):
    delimiter = '$'
    idpattern = r'(?a:[_a-z][_a-z0-9]*)'
    pattern = r"""
            \$(?:
                (?P<escaped>\$) |
                (?P<named>%(id)s) |
                \[(?P<braced>%(id)s)\] |
                (?P<invalid>)
            )
        """ % {'id': idpattern}


_ansi = {}
for key, value in Fore.__dict__.items():
    _ansi['F' + key.lower()] = value
for key, value in Back.__dict__.items():
    _ansi['B' + key.lower()] = value
for key, value in Style.__dict__.items():
    _ansi['S' + key.lower()] = value
_void_ansi = _ansi.copy()
for key, value in _void_ansi.items():
    _void_ansi[key] = ''
def colored_string(src_str:str):
    result = BetterTemplate(src_str).substitute(_ansi) + Style.RESET_ALL
    return result

class _C:
    def __pow__(self, power: str, modulo=None):
        return colored_string(power)
c = _C()


def get_width(string: str):
    return Text.from_ansi(string).cell_len


def embed(src_str:str, embed_str:str, side:Literal['l', 'r', 'r_against_l']= 'r_against_l'):
    string_lines = src_str.splitlines()
    embed_lines = embed_str.splitlines()
    string_width = max(get_width(i) for i in string_lines)
    embed_width = max(get_width(i) for i in embed_lines)
    height = max(len(embed_lines), len(string_lines))
    for _ in range(max(height - len(string_lines), 0)): string_lines.append('')
    for _ in range(max(height - len(embed_lines), 0)): embed_lines.append('')
    result = []
    match side:
        case 'l':
            embed_lines = [i + (embed_width - get_width(i)) * ' ' for i in embed_lines]
            result = [i + j for i, j in zip(embed_lines, string_lines)]
        case 'r':
            string_lines = [i + (string_width - get_width(i)) * ' ' for i in string_lines]
            result = [i + j for i, j in zip(string_lines, embed_lines)]
        case 'r_against_l':
            string_lines = [i + (string_width - get_width(i)) * ' ' for i in string_lines]
            result = [i + j if i.strip() else j for i, j in zip(string_lines, embed_lines)]
        case val:
            raise ValueError(f'Invalid value {val}')
    result = '\n'.join(result)
    return result


class Border:
    def __init__(self, border_style:str, *, min_width=0, spacial_notation:dict=None, style:tuple[str, ...] | str=None):
        if spacial_notation is None:
            spacial_notation = {'_': ''}
        border_style = [i.split() for i in border_style.splitlines() if i.strip()]
        if not len(border_style) == 3:
            raise BorderError('Style syntax error.')
        if not (len(border_style[0]) == 3 and len(border_style[1]) == 2 and len(border_style[2]) == 3):
            raise BorderError('Style syntax error.')
        self.left = border_style[1][0]
        self.right = border_style[1][1]
        self.top = border_style[0][1]
        self.bottom = border_style[2][1]
        self.left_top = border_style[0][0]
        self.right_top = border_style[0][2]
        self.left_bottom = border_style[2][0]
        self.right_bottom = border_style[2][2]
        for k, v in self.__dict__.items():
            if v in spacial_notation:
                setattr(self, k, spacial_notation[v])
        if any(get_width(i) > 1 for i in [self.bottom, self.top]):
            raise CharWidthError('Width of bottom character or top charactor bigger than 1.')
        self.min_width = min_width
        self.style = style

def _simple_style(string:str, style:tuple[str, ...] | str | None):
    if not (isinstance(style, str) or isinstance(style, tuple) or (style is None)): raise TypeError(f'Invalid type {style.__class__.__name__}')
    return colored_string(''.join(f'$[{i}]' for i in (style if isinstance(style, tuple) else (style,))) + string) if style is not None else string

def add_border(src_str:str, border:Border):
    src_str_lines = src_str.splitlines()
    width = max(*[get_width(i) for i in src_str_lines], border.min_width)
    src_str_lines = (([_simple_style(top, border.style)] if (top := border.left_top + border.top * width + border.right_top) else [])
                     + [_simple_style(border.left, border.style) + i + (width - get_width(i)) * ' ' + _simple_style(border.right, border.style) for i in src_str_lines]
                     + ([_simple_style(bottom, border.style)] if (bottom := border.left_bottom + border.bottom * width + border.right_bottom) else []))
    return '\n'.join(src_str_lines) + '\n'


def add_indent(src_str:str, width=2):
    return '\n'.join(width * ' ' + i for i in src_str.splitlines())




__all__ = [
    'embed',
    'Border',
    'add_border',
    'add_indent',
    'colored_string',
    'c',
    'get_width'
]
