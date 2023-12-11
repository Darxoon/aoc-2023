from dataclasses import dataclass
from itertools import combinations
from re import Match, finditer

counter = 0

GALAXY_EXPAND = 1000000 - 1

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

    def get_distance(self, other: "Rect", expanded_colums: list[bool], expanded_rows: list[bool]) -> int:
        min_x = min(self.x, other.x)
        max_x = max(self.x, other.x)
        
        min_y = min(self.y, other.y)
        max_y = max(self.y, other.y)
        
        dx = abs(other.x - self.x) + expanded_colums[min_x:max_x + 1].count(True) * GALAXY_EXPAND
        dy = abs(other.y - self.y) + expanded_rows[min_y:max_y + 1].count(True) * GALAXY_EXPAND - 1
        
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
    
    lines = input_file.splitlines()
    
    expanded_rows = [line.count('.') == len(line) for line in lines]
    expanded_colums = [True] * len(lines[0])
    
    for line in lines:
        expanded_colums = [expandable_colum and c == '.' for c, expandable_colum in zip(line, expanded_colums)]
    
    # calculate distances
    input_file = '\n'.join(lines)
    field_width = input_file.index('\n') + 1
    
    rects = [Rect.from_match(x, field_width) for x in finditer(r'#', input_file)]
    
    star_pairs = combinations(rects, 2)
    print(sum(a.get_distance(b, expanded_colums, expanded_rows) for a, b in star_pairs))

if __name__ == '__main__':
    main()
