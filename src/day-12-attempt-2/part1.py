def verify_line(line: str, sizes: list[int]) -> bool:
    sizes_iter = iter(sizes)
    
    damaged_counter = 0
    current_size = next(sizes_iter, -1)
    
    for c in line:
        match c:
            case '?':
                raise Exception("Found '?' in verify_line input")
            case '#':
                damaged_counter += 1
            case '.':
                if damaged_counter > 0:
                    if damaged_counter != current_size:
                        return False
                    else:
                        damaged_counter = 0
                        current_size = next(sizes_iter, -1)
    
    if damaged_counter > 0:
        if damaged_counter != current_size:
            return False
        else:
            damaged_counter = 0
            current_size = next(sizes_iter, -1)
    
    return current_size == -1

def get_variation(line: str, id: int) -> str:
    i = -1
    return [
        c if c != '?' else ('#' if id & 1 << (i := i + 1) else '.')
        for c in line
    ]

def bruteforce_line(line: str, sizes: list[int]):
    unknowns = line.count('?')
    possibilities = 2 ** unknowns
    
    variations = [get_variation(line, i) for i in range(possibilities)]
    possible_variations = [verify_line(variation, sizes) for variation in variations].count(True)
    return possible_variations

def bruteforce_unprocessed_line(line: str) -> int:
    sizes_start = line.index(' ')
    sizes = [int(x) for x in line[sizes_start + 1:].split(',')]
    
    return bruteforce_line(line[:sizes_start], sizes)

def main():
    with open('day-12-attempt-2/input.txt', 'r') as f:
        input_file = f.read()
    
    # for line in input_file.splitlines():
    #     print(bruteforce_unprocessed_line(line))
    
    print(sum(bruteforce_unprocessed_line(line) for line in input_file.splitlines()))

if __name__ == "__main__":
    main()