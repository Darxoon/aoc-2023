from math import lcm
from re import findall
from itertools import cycle

def find_node_solution(node_names: list[str],
                       node_destinations: list[tuple[int, int]],
                       instructions: list[int],
                       node: int) -> int:
    instructions_iter = cycle(iter(instructions))
    count = 0
    while not node_names[node].endswith('Z'):
        node = node_destinations[node][next(instructions_iter)]
        count += 1
    
    return count

def main():
    with open('day-8/input.txt', 'r') as f:
        input_file = f.read()
    
    lines = input_file.split('\n')
    instructions = [(1 if c == 'R' else 0) for c in lines[0]]
    
    node_matches = [findall(r'^(\w+) = \((\w+), (\w+)\)$', line)[0] for line in lines[2:]]
    node_names: list[str] = [match[0] for match in node_matches]
    print(f"{node_names=}")
    
    node_destinations = [(node_names.index(match[1]), node_names.index(match[2])) for match in node_matches]
    print(f"{node_destinations=}")
    
    nodes = [i for i, name in enumerate(node_names) if name.endswith('A')]
    
    individual_node_steps = [find_node_solution(node_names, node_destinations, instructions, node) for node in nodes]
    print(lcm(*individual_node_steps))

if __name__ == "__main__":
    main()
