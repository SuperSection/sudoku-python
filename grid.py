from random import sample

GRID_LENGTH = 720
CELL_COUNT = 9
CELL_SIZE = GRID_LENGTH // CELL_COUNT


def create_line_coordinates(cell_size: int) -> list[list[tuple]]:
    """ Creates the x,y coordinates for drwaning the grid lines. """
    points = []
    for y in range(1, 9):
        # horizontal lines (row wise)
        temp = []
        temp.append((0, y * cell_size)) # x,y points [(0, 80), (0, 160), (0, 240), ...]
        temp.append((GRID_LENGTH, y * cell_size)) # x,y points [(720, 80), (720, 160), (720, 240), ...]
        points.append(temp)
        
    for x in range(1, 10):
        # vertical lines (column wise): from 1 to 10, to close the grid on the right side
        temp = []
        temp.append((x * cell_size, 0)) # x,y points [(80, 0), (160, 0), (240, 0), ...]
        temp.append((x * cell_size, GRID_LENGTH)) # x,y points [(80, 720), (160, 720), (240, 720), ...]
        points.append(temp)

    return points



SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE


# pattern for a baseline valid solution
def pattern(row_num: int, col_num: int) -> int:
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE  


# randomize row
def shuffle(s: range) -> list:
    return sample(s, len(s))


# produce board using randomized baseline pattern
def create_grid(sub_grid: int) -> list[list]:
    """ Create the 9x9 grid filled with random numbers. """
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]


def remove_numbers(grid: list[list]) -> None:
    """ Remove numbers from the grid. """
    num_of_cells = GRID_SIZE * GRID_SIZE
    empties = num_of_cells * 3 // 7  # 7 is ideal - higher the number easier the game
    
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0




class Grid:
    def __init__(self, font):
        self.cell_size = CELL_SIZE
        self.num_x_offset = 25
        self.num_y_offset = 12
        self.line_coordinates = create_line_coordinates(self.cell_size)
        self.grid = create_grid(SUB_GRID_SIZE)
        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()
        print(len(self.occupied_cell_coordinates))
        
        self.game_font = font
        
    
    def is_cell_preoccupied(self, col: int, row: int) -> bool:
        """ Check for non-playable cells - preoccupied/initialized cells. """
        for cell in self.occupied_cell_coordinates:
            if cell[0] == row and cell[1] == col:
                return True
        
        return False
    
    
    def get_mouse_click(self, x: int, y: int) -> None:
        """ Get the y,x coordinates for the clicked cell. """
        if x <= GRID_LENGTH:
            grid_x, grid_y = x // self.cell_size, y // self.cell_size
            if not self.is_cell_preoccupied(grid_x, grid_y):
                self.set_cell(grid_x, grid_y, -1)
    
    
    def pre_occupied_cells(self) -> int:
        """ Gather the y,x coordinates for all preoccupied / initialized cells. """
        occupied_cell_coordinates = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] != 0:
                    occupied_cell_coordinates.append((row, col))
        
        return occupied_cell_coordinates
    
    
    def __draw_lines(self, pg, surface) -> None:
        """ Draw the grid lines. """
        for index, point in enumerate(self.line_coordinates):
            if index == 2 or index == 5 or index == 10 or index == 13:
                pg.draw.line(surface, (255, 200, 0), point[0], point[1])
            else:
                pg.draw.line(surface, (0, 50, 0), point[0], point[1])


    def __draw_numbers(self, surface) -> None:
        """ Draw the grid numbers. """
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] != 0:
                    text_surface = self.game_font.render(str(self.get_cell(col, row)), False, (0, 200, 255))
                    surface.blit(text_surface, (col * self.cell_size + self.num_x_offset, row * self.cell_size + self.num_y_offset))
                    
                    
    def draw_all(self, pg, surface) -> None:
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)


    def get_cell(self, col: int, row: int) -> int:
        """ Get a cell value at y,x coordinate. """
        return self.grid[row][col]


    def set_cell(self, col: int, row: int, value: int) -> None:
        """ Set a cell value at y,x coordinate. """
        self.grid[row][col] = value


    def show(self):
        """ Prints the grid row by row to the output. """
        for cell in self.grid:
            print(cell)



if __name__ == "__main__":
    grid = Grid()
    grid.show()
    