from re import findall
from itertools import cycle

def main():
    with open('day-8/input.txt', 'r') as f:
        input_file = f.read()
    
    lines = input_file.split('\n')
    instructions = [(1 if c == 'R' else 0) for c in lines[0]]
    instructions_iter = cycle(iter(instructions))
    
    node_matches = [findall(r'^(\w+) = \((\w+), (\w+)\)$', line)[0] for line in lines[2:]]
    node_names = [match[0] for match in node_matches]
    print(node_names)
    
    node_destinations = [(node_names.index(match[1]), node_names.index(match[2])) for match in node_matches]
    print(node_destinations)
    
    end_index = node_names.index('ZZZ')
    print(end_index)
    
    node = node_names.index('AAA')
    count = 0
    while node != end_index:
        node = node_destinations[node][next(instructions_iter)]
        count += 1
    
    print(node_names[node], node, count)

if __name__ == "__main__":
    main()
