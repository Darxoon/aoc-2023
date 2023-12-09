def extrapolate_numbers(line):
    numbers = [int(x) for x in line.split()]
    number_stack = [numbers]
    
    while not all(x == 0 for x in numbers):
        numbers_diff = [x - numbers[i] for i, x in enumerate(numbers[1:])]
        numbers = numbers_diff
        number_stack.append(numbers)
    
    print(f"{number_stack=}")
    
    numbers.append(0)
    
    # reverse order and without the last element
    for i, numbers in enumerate(number_stack[-2::-1]):
        # numbers one higher in the numbers stack
        prev_numbers = number_stack[-i - 1]
        numbers.append(numbers[-1] + prev_numbers[-1])
    
    return number_stack[0][-1]

def main():
    with open('day-9/input.txt', 'r') as f:
        input_file = f.read()
    
    lines = input_file.splitlines()
    
    print(sum(extrapolate_numbers(line) for line in lines))

if __name__ == "__main__":
    main()