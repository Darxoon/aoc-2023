from dataclasses import dataclass, field
from random import randint
import cProfile

@dataclass
class Direction:
    x: int
    y: int
    
    def opposite(self):
        return Direction(-self.x, -self.y)

NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
WEST = Direction(-1, 0)
EAST = Direction(1, 0)

@dataclass
class Tile:
    north: bool
    south: bool
    east: bool
    west: bool
    
    start: bool = False
    num: int = field(default_factory=lambda: randint(0, 2147483647))
    
    def from_char(c):
        match c:
            case '|':
                return Tile(True, True, False, False)
            case '-':
                return Tile(False, False, True, True)
            case 'L':
                return Tile(True, False, True, False)
            case 'J':
                return Tile(True, False, False, True)
            case '7':
                return Tile(False, True, False, True)
            case 'F':
                return Tile(False, True, True, False)
            case 'S':
                return Tile(True, True, True, True, True)
            case _:
                return None
    
    def get_directions(self):
        if self.north:
            yield NORTH
        if self.south:
            yield SOUTH
        if self.east:
            yield EAST
        if self.west:
            yield WEST

def get_all_tiles(tiles: list[list[Tile | None]], start_x, start_y, start_direction) -> list[Tile]:
    is_starting = True
    x = start_x
    y = start_y
    direction: Direction = start_direction
    current_tile: Tile = tiles[y][x]
    
    while not (current_tile and current_tile.start and not is_starting):
        # print(f"{x=} {y=} {direction=} {current_tile=}")
        yield current_tile
        
        x += direction.x
        y += direction.y
        current_tile = tiles[y][x]
        is_starting = False
        
        opposite = direction.opposite()
        
        direction = next(d for d in current_tile.get_directions() if d != opposite)

def get_enclosed_spaces(all_tiles: list[Tile], line: list[Tile | None]) -> int:
    accumulator = 0
    is_inside = False
    start_tile = None
    end_tile = None
    
    for tile in line:
        is_pipe_tile = tile and tile in all_tiles
        
        if is_pipe_tile:
            if start_tile is None:
                start_tile = tile
                end_tile = tile
            
            elif tile.west:
                end_tile = tile
            
            if not tile.east:
                if start_tile == end_tile or start_tile.north != end_tile.north:
                    is_inside = not is_inside
                
                start_tile = None
                end_tile = None
        
        elif is_inside:            
            accumulator += 1
    
    print(accumulator)
    return accumulator

def main():
    with open('day-10/input.txt', 'r') as f:
        input_file = f.read()
    
    lines = input_file.splitlines()
    tiles = [[Tile.from_char(c) for c in line] for line in lines]
    
    # find 'S' tile
    start_x, start_y, start_tile = next((j, i, tile) for i, line in enumerate(tiles)
                                        for j, tile in enumerate(line) if tile and tile.start)
    
    
    start_direction = next(d for d in start_tile.get_directions()
                           if tiles[start_y + d.y][start_x + d.x]
                           and d.opposite() in tiles[start_y + d.y][start_x + d.x].get_directions())
    
    all_tiles = list(get_all_tiles(tiles, start_x, start_y, start_direction))
    
    # fix 'S' tile directions
    if not (tiles[start_y - 1][start_x] and tiles[start_y - 1][start_x].south):
        start_tile.north = False
    if not (tiles[start_y + 1][start_x] and tiles[start_y + 1][start_x].north):
        start_tile.south = False
    if not (tiles[start_y][start_x - 1] and tiles[start_y][start_x - 1].east):
        start_tile.west = False
    if not (tiles[start_y][start_x + 1] and tiles[start_y][start_x + 1].west):
        start_tile.east = False
    
    print(sum(get_enclosed_spaces(all_tiles, line) for line in tiles))

if __name__ == "__main__":
    cProfile.run('main()')
