#/usr/bin/env python3
from re import findall
from dataclasses import dataclass
from typing import Iterable

@dataclass
class Set:
    red: int
    green: int
    blue: int
    
    def from_str(string: str):
        matches = findall('(\d+) (red|blue|green)', string)
        
        red = 0
        green = 0
        blue = 0
        
        for count, color in matches:
            match color:
                case "red": red = int(count)
                case "green": green = int(count)
                case "blue": blue = int(count)
        
        return Set(red, green, blue)
    
    def max(sets: list["Set"]) -> "Set":
        red = max(x.red for x in sets)
        green = max(x.green for x in sets)
        blue = max(x.blue for x in sets)
        return Set(red, green, blue)
    
    def power(self) -> int:
        return self.red * self.green * self.blue


def analyze_game(line: str) -> int:
    if not line:
        return 0
    
    game_id = int(findall("^Game (\d+):", line)[0])
    set_strings = line[line.index(':') + 1:].split(';')
    
    min_required_set = Set.max([Set.from_str(string) for string in set_strings])
    print(f"{game_id} {min_required_set}")
    
    return min_required_set.power()
    

def main():
    with open('day-2/input.txt', 'r') as f:
        input_file = f.read()
    
    lines = input_file.split('\n')
    
    powers = sum(analyze_game(line) for line in lines)
    print("sum of possible games:", powers)


if __name__ == "__main__":
    main()
