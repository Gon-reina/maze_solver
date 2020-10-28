
"""
The maze class can generate a maze of size N cells by using the depth-first search algorithm using backtracking.
It first generates a grid and then moves from cell to a randomly chosen neighbouring cell as long as there are valid neighbours to choose.
If it reaches a dead end it backtracks until it finds a cell with valid neighbours.
It repeates this process until it has visited all the cells in the maze.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os

class Maze:
    def __init__(self, N=5):
        self.N = N
        # Create a list of Cell positions
        self.cells = []
        for ny in range(2*self.N):
            if ny % 2 !=0:
                self.cells.append(ny)
        # Create a maze map with all the cells
        self.maze_map = self.create_maze_map()
        # Draw a maze of size N as a binary array
        self.images = []
        self.draw_maze()

        
    def draw_maze(self):
        path = os.getcwd()
        path = path + '\\frames'
        if os.path.exists(path+"\\frames")==True:
            os.mkdir(path)
        # Create a grid to later knock down the walls
        self.grid = self.creategrid()
        # Choose a random cell on the right size to start
        mx = 0
        my = np.random.randint(0,self.N)
        # Knock down the entrance wall by setting it to 0
        self.grid[self.maze_map[my][mx].ny][0] = 0
        plt.imshow(self.grid, cmap = "Blues")
        plt.axis('off')
        name = "frames\Maze{}.png".format(0)
        plt.savefig(name, bbox_inches='tight')
        im = Image.open(name)
        self.images.append(im)
        
        
        path = []
        # Make the chosen start coordinates the current cell
        current_cell = self.maze_map[my][mx]
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
            if current_cell.my-next_cell.my == 1:
                # Knock down north wall
                self.grid[current_cell.ny-1][current_cell.nx] = (current_cell.nx)/((3*(self.N-1)))
            if current_cell.my-next_cell.my == -1:
                # Knock down south wall
                self.grid[current_cell.ny+1][current_cell.nx] = (current_cell.nx)/((3*(self.N-1)))
            if current_cell.mx-next_cell.mx == 1:
                # Knock down west wall
                self.grid[current_cell.ny][current_cell.nx-1] = (current_cell.nx-1)/(((3*self.N-1)))
            if current_cell.mx-next_cell.mx == -1:
                # Knock down east wall
                self.grid[current_cell.ny][current_cell.nx+1] = (current_cell.nx+1)/(((3*self.N-1)))
            
            self.grid[current_cell.ny][current_cell.nx] = (current_cell.nx)/((3*self.N-1))
            plt.imshow(self.grid, cmap = "Blues")
            plt.axis('off')
            name = "frames\Maze{}.png".format(Nv)
            plt.savefig(name, bbox_inches='tight')
            im = Image.open(name)
            self.images.append(im)
            
            # Make the next cell the current cell and mark it as visited
            current_cell = next_cell
            current_cell.visit()
            Nv = Nv+1
            # Append it to the path
            path.append(current_cell)
            
        # Once it is finished it chooses a random exit on the left side of the maze
        my = np.random.randint(0,self.N)
        self.grid[self.maze_map[my][-1].ny][-1] = (self.maze_map[-1][-1].nx)/((3*(self.N-1)))
        plt.imshow(self.grid, cmap = "Blues")
        plt.axis('off')
        name = "frames\Maze{}.png".format(Nv+1)
        plt.savefig(name, bbox_inches='tight')
        im = Image.open(name)
        self.images.append(im)
        # Add some padding to the edges of thhe maze
        pad = 2
        final_grid = np.zeros([self.grid.shape[0]+2*pad,self.grid.shape[1]+2*pad])
        final_grid[pad:-pad,pad:-pad] = self.grid
        self.grid = final_grid
        
        self.images[0].save('maze_draw.gif', save_all=True, append_images=self.images[1:], optimize=False, duration=180, loop=0)
        
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
        my = Cell.my
        mx = Cell.mx
        neighbours = []
        if my-1>=0 and self.maze_map[my-1][mx].Visited == False:
            neighbours.append(self.maze_map[my-1][mx])
        if my+1<=len(self.maze_map)-1 and  self.maze_map[my+1][mx].Visited == False:
            neighbours.append(self.maze_map[my+1][mx])
        if mx-1>=0 and self.maze_map[my][mx-1].Visited == False:
            neighbours.append(self.maze_map[my][mx-1])
        if mx+1<=len(self.maze_map[0])-1 and self.maze_map[my][mx+1].Visited == False:
            neighbours.append(self.maze_map[my][mx+1])
        # If the cell doent have any valid neighbours return a 0
        if not neighbours:
            neighbours = 0
            
        return neighbours
    
    def create_maze_map(self):
        # Generate maze map of cells
        maze_map = [[Cell() for n in range(self.N)] for n in range(self.N)]
        for my,ny in enumerate(self.cells):
            for mx,nx in enumerate(self.cells):
                maze_map[my][mx].grid_coords(ny, nx)
                maze_map[my][mx].map_coords(my, mx)
                
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
    def map_coords(self,my,mx):
        self.my = my
        self.mx = mx