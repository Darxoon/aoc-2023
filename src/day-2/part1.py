#/usr/bin/env python3
from re import findall
from dataclasses import dataclass

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
    
    def is_lte(self, other: "Set"):
        return (self.red <= other.red
                and self.green <= other.green
                and self.blue <= other.blue)


def analyze_game(line: str, ruleset: Set):
    if not line:
        return None
    
    game_id = int(findall("^Game (\d+):", line)[0])
    set_strings = line[line.index(':') + 1:].split(';')
    is_possible = all(Set.from_str(string).is_lte(ruleset) for string in set_strings)
    print(f"{game_id} {is_possible=}")
    
    return game_id if is_possible else None
    

def main():
    with open('day-2/input.txt', 'r') as f:
        input_file = f.read()
    
    ruleset = Set(12, 13, 14)
    lines = input_file.split('\n')
    
    games_and_none = (analyze_game(line, ruleset) for line in lines)
    possible_games = (x for x in games_and_none if x is not None)
    print("sum of possible games:", sum(possible_games))


if __name__ == "__main__":
    main()
