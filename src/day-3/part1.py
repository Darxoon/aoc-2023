from dataclasses import dataclass
import re

counter = 0

@dataclass
class Rect:
    content: int | str
    id: int
    x1: int
    x2: int
    y: int
    
    def __init__(self, match: re.Match, field_width: int):
        global counter
        
        if match.group(1) is not None:
            self.content = int(match.group(1))
        else:
            self.content = match.group(2)
        
        self.id = counter
        self.y = match.start(0) // field_width
        self.x1 = match.start(0) % field_width
        self.x2 = match.end(0) % field_width - 1
        
        counter += 1
    
    def touches(self, other: "Rect"):
        return (self.x1 - 1 <= other.x2
                and self.x2 + 1 >= other.x1
                and self.y - 1 <= other.y
                and self.y + 1 >= other.y)

def woah(x):
    print(f"==== {x}")
    return x

def main():
    with open('day-3/main.txt', 'r') as f:
        input_file = f.read()
    
    field_width = input_file.index('\n') + 1
    
    rects = [Rect(x, field_width) for x in re.finditer(r'(\d+)|([^.\n])', input_file)]
    
    numbers = [rect for rect in rects if isinstance(rect.content, int)]
    chars = [rect for rect in rects if isinstance(rect.content, str)]
    print(f"{numbers=}\n")
    print(f"{chars=}\n")
    
    relevant_numbers = (num_rect.content for num_rect in numbers if any([num_rect.touches(char) for char in chars]))
    print(sum(relevant_numbers))

if __name__ == '__main__':
    main()
