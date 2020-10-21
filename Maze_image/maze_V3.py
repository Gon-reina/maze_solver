
"""
The maze class can generate a maze of size N cells by using the depth-first search algorithm using backtracking.
It first generates a grid and then moves from cell to a randomly chosen neighbouring cell as long as there are valid neighbours to choose.
If it reaches a dead end it backtracks until it finds a cell with valid neighbours.
It repeates this process until it has visited all the cells in the maze.
"""
import numpy as np
import matplotlib.pyplot as plt

class Maze:
    def __init__(self, N=5):
        self.N = N
        # Create a maze map with all the cells
        self.maze_map = self.create_maze_map()
        # Draw a maze of size N as a binary array
        self.draw_maze()
        
    def draw_maze(self):
        # Create a grid to later knock down the walls
        self.grid = self.creategrid()
        # Create a list of the coordinates of the walls
        walls = []
        for ny in range(2*self.N):
            if ny % 2 !=0:
                walls.append(ny)
        # Choose a random cell on the right size to start
        nx = 0
        ny = np.random.randint(0,self.N-1)
        # Knock down the entrance wall by setting it to 0
        self.grid[walls[ny]][nx] = 0
        path = []
        # Make the chosen start coordinates the current cell
        current_cell = self.maze_map[ny][nx]
        # Mark it as visited
        current_cell.visit()
        CellNumber = self.N**2
        Nv = 1
        # Add the current cell to the path taken
        path.append(current_cell)
        # Repeat this process untill all cells have been visited
        while CellNumber > Nv:
            # Find valid neighbours for thte current cell
            neighbours = self.find_neighbours(current_cell)
            # If it does not have any valid neighbours 
            while neighbours == 0:
                # Backtrack until a cell with valid neighbours is found
                path.remove(current_cell)
                current_cell = path[-1]
                neighbours = self.find_neighbours(current_cell)
            # Choose the next cell randomly
            next_cell = np.random.choice(neighbours)
            if current_cell.ny-next_cell.ny == 1:
                # Knock down north wall
                self.grid[walls[current_cell.ny]-1][walls[current_cell.nx]] = 0
            if current_cell.ny-next_cell.ny == -1:
                # Knock down south wall
                self.grid[walls[current_cell.ny]+1][walls[current_cell.nx]] = 0
            if current_cell.nx-next_cell.nx == 1:
                # Knock down west wall
                self.grid[walls[current_cell.ny]][walls[current_cell.nx]-1] = 0
            if current_cell.nx-next_cell.nx == -1:
                # Knock down east wall
                self.grid[walls[current_cell.ny]][walls[current_cell.nx]+1] = 0
            # Make the next cell the current cell and mark it as visited
            current_cell = next_cell
            current_cell.visit()
            Nv = Nv+1
            # Append it to the path
            path.append(current_cell)
        # Once it is finished it chooses a random exit on the left side of the maze
        ny = np.random.randint(0,self.N-1)
        self.grid[walls[ny]][-1] = 0
        # Add some padding to the edges of thhe maze
        pad = 2
        final_grid = np.zeros([self.grid.shape[0]+2*pad,self.grid.shape[1]+2*pad])
        final_grid[pad:-pad,pad:-pad] = self.grid
        self.grid = final_grid
        
    def creategrid(self):
        # This creates a grid of 0 and 1 where 1 is a wall and 0 is the path
        grid = np.zeros([self.N+(self.N-1)+2,self.N+(self.N-1)+2])
        for ny in range(self.N+(self.N-1)+2):
            if ny % 2 ==0:
                grid[ny,:] = 1
                grid[:,ny] = 1
        
        return grid
        
    def find_neighbours(self,Cell):
        # This function finds all valid neighbours for a cell
        # For the neighbours to be valid they have to be unvisited and inside the maze
        ny = Cell.ny
        nx = Cell.nx
        neighbours = []
        if ny-1>=0 and self.maze_map[ny-1][nx].Visited == False:
            neighbours.append(self.maze_map[ny-1][nx])
        if ny+1<=len(self.maze_map)-1 and  self.maze_map[ny+1][nx].Visited == False:
            neighbours.append(self.maze_map[ny+1][nx])
        if nx-1>=0 and self.maze_map[ny][nx-1].Visited == False:
            neighbours.append(self.maze_map[ny][nx-1])
        if nx+1<=len(self.maze_map[0])-1 and self.maze_map[ny][nx+1].Visited == False:
            neighbours.append(self.maze_map[ny][nx+1])
        # If the cell doent have any valid neighbours return a 0
        if not neighbours:
            neighbours = 0
            
        return neighbours
    
    def create_maze_map(self):
        # Generate maze map of cells
        maze_map = [[Cell() for n in range(self.N)] for n in range(self.N)]
        for ny in range(len(maze_map)):
            for nx in range(len(maze_map[0])):
                # Define gird coordinates for every cell
                maze_map[ny][nx].grid_coords(ny,nx)

        return maze_map

class Cell:
    def __init__(self):
        self.Visited = False
    
    def visit(self):
        self.Visited = True
        
    def grid_coords(self,ny,nx):
        # Define grid coordinates for the cell
        self.ny = ny
        self.nx = nx
        
maze = Maze(40)
img = plt.imshow(maze.grid, cmap = "summer")
plt.axis('off')
plt.savefig("Maze.png", bbox_inches='tight')


