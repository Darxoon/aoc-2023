from re import findall

def hash(input_string: str) -> int:
    accumulator = 0
    
    for c in input_string:
        accumulator = (accumulator + ord(c)) * 17 % 256
    
    return accumulator

def focusing_power_of_box(box: list[tuple[str, int]], box_index: int) -> int:
    return (box_index + 1) * sum((i + 1) * value for i, (label, value) in enumerate(box))

def main():
    with open('day-15/input.txt', 'r') as f:
        input_string = f.read().replace('\n', '')
    
    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]
    
    for instruction in input_string.split(','):
        label, value_str = findall(r"^(\w+)(?:=(\d+)|-)$", instruction)[0]
        
        box = boxes[hash(label)]  
        entry_index = next((i for i, (entry_label, _) in enumerate(box) if entry_label == label), None)
        
        # print(label, hash(label), f"{'deleting ' if not value_str else ''}{entry_index=}")
        
        if len(value_str) > 0:
            if entry_index is not None:
                # replace
                box[entry_index] = label, int(value_str)
            else:
                # insert
                boxes[hash(label)].append((label, int(value_str)))
        else:
            if entry_index is not None:
                # delete
                box.pop(entry_index)
        
        # for i, box in ((i, box) for i, box in enumerate(boxes) if len(box) > 0):
        #     print(i, box)
    
    print(sum(focusing_power_of_box(box, i) for i, box in enumerate(boxes)))

if __name__ == "__main__":
    main()
