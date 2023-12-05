from dataclasses import dataclass
from itertools import islice
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

def get_seed_locations(seeds: list[int], maps: list[AlmanacMap]):
    resource_type = 'seed'
    resource_nums = seeds
    
    while resource_type != 'location':
        applicable_map = next(x for x in maps if x.map_from == resource_type)
        print(f'moving from {resource_type} to {applicable_map.map_to}')
        
        resource_type = applicable_map.map_to
        resource_nums = [applicable_map.map(x) for x in resource_nums]
    
    return resource_nums

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

def iterate_seeds(seed_rules):
    for seed_start, seed_count in seed_rules:
        print(f"iterating through rule {seed_start} {seed_count}")
        for i in range(seed_count):
            yield seed_start + i

def woah(x, y):
    print(x, y)
    return x

def main():
    # this code takes too long to finish
    # see day-5-attempt-2 instead (and make sure to run that in Release mode)
    
    with open("day-5/input.txt", "r") as f:
        input_file = f.read()
    
    seed_rules = list(chunk((int(seed) for seed in input_file[input_file.index(':') + 2:input_file.index('\n')].split(' ')), 2))
    seeds = list(range(seed_rules[0][0], seed_rules[0][0] + seed_rules[0][1]))
    print("seeds generated")
    
    maps = [AlmanacMap.from_string(block) for block in input_file[input_file.index('\n') + 2:].split('\n\n')]
    print("maps parsed")
    
    print(min(get_seed_locations(seeds, maps)))

if __name__ == "__main__":
    main()