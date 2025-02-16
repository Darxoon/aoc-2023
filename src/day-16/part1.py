UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

FORWARD_SLASH_MIRROR = [RIGHT, UP, LEFT, DOWN]
BACKWARD_SLASH_MIRROR = [LEFT, DOWN, RIGHT, UP]

VERTICAL_MOVEMENT = [-1, 0, 1, 0]
HORIZONTAL_MOVEMENT = [0, 1, 0, -1]

def main():
    with open('day-16/input.txt', 'r') as f:
        input_file = f.read()
    
    lines = input_file.splitlines()
    
    height = len(lines)
    width = len(lines[0])
    
    energized: list[bool] = [False] * (len(lines[0]) * len(lines))
    horizontal: list[bool] = [False] * (len(lines[0]) * len(lines))
    vertical: list[bool] = [False] * (len(lines[0]) * len(lines))
    
    beam_x = 0
    beam_y = 0
    beam_direction = RIGHT
    
    other_beams: list[tuple[int, int, int]] = []
    
    while True:
        char = lines[beam_y][beam_x]
        moving_vertically = beam_direction % 2 == 0
        
        match char:
            case '-':
                if moving_vertically:
                    other_beams.append((beam_x, beam_y, LEFT))
                    beam_direction = RIGHT
            case '|':
                if not moving_vertically:
                    other_beams.append((beam_x, beam_y, UP))
                    beam_direction = DOWN
            case '/':
                # print(f'touched / at {beam_x}, {beam_y} with {beam_direction}')
                beam_direction = FORWARD_SLASH_MIRROR[beam_direction]
            case '\\':
                # print(f'touched \\ at {beam_x}, {beam_y} with {beam_direction}')
                beam_direction = BACKWARD_SLASH_MIRROR[beam_direction]
        
        moving_vertically = beam_direction % 2 == 0
        
        energized[beam_y * height + beam_x] = True
        
        # print(beam_direction, moving_vertically, VERTICAL_MOVEMENT[beam_direction], HORIZONTAL_MOVEMENT[beam_direction])
        
        if moving_vertically:
            vertical[beam_y * height + beam_x] = True
            beam_y += VERTICAL_MOVEMENT[beam_direction]
        else:
            horizontal[beam_y * height + beam_x] = True
            beam_x += HORIZONTAL_MOVEMENT[beam_direction]
        
        if (beam_x < 0 or beam_x >= width or beam_y < 0 or beam_y >= height
            or (vertical[beam_y * height + beam_x] and moving_vertically)
            or (horizontal[beam_y * height + beam_x] and not moving_vertically)):
            
            if len(other_beams) > 0:
                beam_x, beam_y, beam_direction = other_beams.pop()
                print(energized.count(True))
            else:
                break
    
    print(energized.count(True))

if __name__ == "__main__":
    main()
