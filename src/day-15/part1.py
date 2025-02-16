def hash(input_string: str) -> int:
    accumulator = 0
    
    for c in input_string:
        accumulator = (accumulator + ord(c)) * 17 % 256
    
    return accumulator

def main():
    with open('day-15/input.txt', 'r') as f:
        input_string = f.read().replace('\n', '')
    
    hashes = sum(hash(x) for x in input_string.split(','))
    
    print(hashes)

if __name__ == "__main__":
    main()
