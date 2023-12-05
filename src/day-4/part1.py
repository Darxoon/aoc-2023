from dataclasses import dataclass
import re

@dataclass
class Card:
    id: int
    winning_numbers: list[int]
    numbers: list[int]
    
    def __init__(self, line: str):
        self.id = int(re.findall(r"^Card +(\d+):", line)[0])
        winning_string, numbers_string = line[line.index(':') + 1:].split('|')
        self.winning_numbers = [int(x) for x in winning_string.split(' ') if x != ""]
        self.numbers = [int(x) for x in numbers_string.split(' ') if x != ""]
    
    def score(self) -> int:
        result = 0
        
        for num in self.numbers:
            if num in self.winning_numbers:
                if result != 0:
                    result *= 2
                else:
                    result = 1
        
        print(f"{self.id} {result=}")
        return result

def main():
    with open('day-4/main.txt', 'r') as f:
        input_file = f.read()
    
    cards = [Card(line) for line in input_file.split('\n')]
    total_score = sum(card.score() for card in cards)
    print(total_score)

if __name__ == "__main__":
    main()