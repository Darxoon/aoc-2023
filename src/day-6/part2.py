from re import findall

def main():
    with open('day-6/input.txt', 'r') as f:
        input_file = f.read()
    
    lines = input_file.split('\n')
    
    time, record = (int("".join(findall(r'\d', line))) for line in lines)
    
    print(f"{time = }, {record = }")
    
    # first solution, took about 5 seconds to complete
    # total = [i * (time - i) > record for i in range(time)].count(True)
    # print(total)
    
    # second solution, takes about 0.8 seconds to complete
    first = next(i for i in range(time) if i * (time - i) > record)
    last = next(i for i in range(time)[::-1] if i * (time - i) > record)
    print(last - first + 1)

if __name__ == "__main__":
    main()
