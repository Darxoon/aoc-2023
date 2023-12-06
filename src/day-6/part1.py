from functools import reduce
from operator import mul

def main():
    with open('day-6/input.txt', 'r') as f:
        input_file = f.read()
    
    lines = input_file.split('\n')
    
    times, records = ([int(x) for x in line[line.index(':') + 1:].split()] for line in lines)
    
    total = reduce(mul, ([i * (time - i) > record for i in range(time)].count(True) for time, record in zip(times, records)))
    print(total)
    
    # for time, record in zip(times, records):
    #     options = [i * (time - i) > record for i in range(time)].count(True)
    #     print(time, record, options)

if __name__ == "__main__":
    main()
