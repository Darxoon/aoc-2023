from dataclasses import dataclass
from typing import Dict
from re import findall

@dataclass
class Rule:
    source_start: int
    destination_start: int
    count: int
    
    def match(self, input: int):
        is_in_bounds = self.source_start <= input < self.source_start + self.count
        
        if is_in_bounds:
            return self.destination_start + input - self.source_start
        else:
            return None

@dataclass
class AlmanacMap:
    map_from: str
    map_to: str
    rules: list[Rule]
    
    def from_string(input: str) -> "AlmanacMap":
        map_from, map_to = findall(r"^(\w+)-to-(\w+) map:", input)[0]
        rules = []
        
        lines = input.split('\n')[1:]
        
        for line in lines:
            destination_start, source_start, line_map_length = (int(x) for x in line.split(' '))
            
            rules.append(Rule(source_start, destination_start, line_map_length))
        
        return AlmanacMap(map_from, map_to, rules)
    
    def map(self, input: int) -> int:
        rule_matches = (rule.match(input) for rule in self.rules)
        return next((match for match in rule_matches if match is not None), input)

def get_seed_location(seed: int, maps: list[AlmanacMap]):
    resource_type = 'seed'
    resource_num = seed
    
    while resource_type != 'location':
        applicable_map = next(x for x in maps if x.map_from == resource_type)
        
        resource_type = applicable_map.map_to
        resource_num = applicable_map.map(resource_num)
    
    return resource_num

def main():
    with open("day-5/input.txt", "r") as f:
        input_file = f.read()
    
    seeds = [int(seed) for seed in input_file[input_file.index(':') + 2:input_file.index('\n')].split(' ')]
    maps = [AlmanacMap.from_string(block) for block in input_file[input_file.index('\n') + 2:].split('\n\n')]
    print(min(get_seed_location(seed, maps) for seed in seeds))

if __name__ == "__main__":
    main()