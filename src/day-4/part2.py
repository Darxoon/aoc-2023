from dataclasses import dataclass
import re

@dataclass
class Card:
    id: int
    count: int
    winning_numbers: list[int]
    numbers: list[int]
    
    def __init__(self, line: str):
        self.id = int(re.findall(r"^Card +(\d+):", line)[0])
        self.count = 1
        
        winning_string, numbers_string = line[line.index(':') + 1:].split('|')
        self.winning_numbers = [int(x) for x in winning_string.split(' ') if x != ""]
        self.numbers = [int(x) for x in numbers_string.split(' ') if x != ""]
        
    def win_card_prize(self, cards: list["Card"]) -> int:
        wins = [num in self.winning_numbers for num in self.numbers].count(True)
        
        for i in range(wins):
            cards[self.id + i].count += self.count
        
        print(f"{self.id} {wins=} won_cards={[self.id + 1 + i for i in range(wins)]}")
        return wins

def main():
    with open('day-4/main.txt', 'r') as f:
        input_file = f.read()
    
    cards = [Card(line) for line in input_file.split('\n')]
    
    for card in cards:
        card.win_card_prize(cards)
    
    print([card.count for card in cards])
    print(sum(card.count for card in cards))

if __name__ == "__main__":
    main()