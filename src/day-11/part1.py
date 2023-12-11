from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from math import floor
from re import Match, finditer

counter = 0

@dataclass
class Rect:
    id: int
    x: int
    y: int
    
    def from_match(match: Match, field_width: int):
        global counter
        
        id = counter
        x = match.start(0) % field_width
        y = match.start(0) // field_width
        
        counter += 1
        return Rect(id, x, y)

    def get_distance(self, other: "Rect") -> int:
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y) - 1
        
        return dy + dx + 1

def expand_line(line: str, expandable_colums: list[bool]) -> str:
    result = ""
    
    for i, c in enumerate(line):
        if expandable_colums[i]:
            result += '..'
        else:
            result += c
    
    return result

def main():
    with open('day-11/input.txt', 'r') as f:
        input_file = f.read()
    
    # expand columns
    lines = input_file.splitlines()
    expandable_colums = [True] * len(lines[0])
    
    for line in lines:
        expandable_colums = [expandable_colum and c == '.' for c, expandable_colum in zip(line, expandable_colums)]
    
    lines = [expand_line(line, expandable_colums) for line in lines]
    
    # expand rows
    for i in range(len(lines))[::-1]:
        if lines[i].count('.') == len(lines[i]):
            lines.insert(i, lines[i])
    
    # calculate distances
    input_file = '\n'.join(lines)
    field_width = input_file.index('\n') + 1
    
    rects = [Rect.from_match(x, field_width) for x in finditer(r'#', input_file)]
    
    star_pairs = combinations(rects, 2)
    print(sum(a.get_distance(b) for a, b in star_pairs))

if __name__ == '__main__':
    main()
