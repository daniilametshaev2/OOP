import os
os.system('color')
from enum import Enum
from typing import Tuple

class Color(Enum):
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

class Printer:
    def __init__(self, color: Color = Color.WHITE, position: Tuple[int,int]=(0,0),
                 symbol: str='*', font_file: str='font_5.txt'):
        self.color = color
        self.position = position
        self.symbol = symbol
        self.load_font(font_file)

    def load_font(self, font_file: str):
        self.font = {}
        with open(font_file, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f]
        i = 0
        while i < len(lines):
            if lines[i].strip() == '':
                i += 1
                continue
            char = lines[i].strip()
            i += 1
            # определяем высоту шрифта по первой букве
            char_lines = []
            while i < len(lines) and lines[i].strip() != '':
                char_lines.append(lines[i])
                i += 1
            self.font[char.upper()] = char_lines
        self.height = max(len(l) for l in self.font.values()) if self.font else 5

    @staticmethod
    def move_cursor(x:int, y:int) -> str:
        return f"\033[{y};{x}H"

    @classmethod
    def print(cls, text: str, color: Color = Color.WHITE,
              position: Tuple[int,int]=(0,0), symbol: str='*',
              font_file: str='font_5.txt'):
        printer = cls(color, position, symbol, font_file)
        printer._print_text(text, position)

    def _print_text(self, text: str, position: Tuple[int,int]):
        x, y = position
        text = text.upper()
        lines = ['' for _ in range(self.height)]
        for char in text:
            if char in self.font:
                char_lines = self.font[char]
                for i in range(self.height):
                    line = char_lines[i] if i < len(char_lines) else ' ' * len(char_lines[0])
                    lines[i] += line.replace('*', self.symbol) + '  '
            else:
                for i in range(self.height):
                    lines[i] += ' ' * (len(next(iter(self.font.values()))[0]) + 2)
        for i, line in enumerate(lines):
            print(f"{self.color.value}{self.move_cursor(x, y+i)}{line}{Color.RESET.value}", end='')
        print()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Color.RESET.value, end='')

Printer.print(
    "HELLO",                
    color=Color.RED,         
    position=(10, 5),        
    symbol='#',              
    font_file="font_5.txt"   
)

Printer.print(
    "WORLD",
    color=Color.BLUE,
    position=(10, 12),       
    symbol='*',
    font_file="font_7.txt"
)


with Printer(Color.GREEN, position=(10, 20), symbol='%', font_file="font_5.txt") as printer:
    printer._print_text("BYE", (10, 20))
    printer._print_text("WORLD", (10, 27))
