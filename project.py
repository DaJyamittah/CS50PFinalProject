"""
Final Project for CS50P edx
Conway's Game of Life with a tkinter GUI.
Animate and 3D Plot from starting state
"""
import tkinter as tk
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np


def inspect(board, element_row, element_col): 
    """Returns a list of neighboring elements."""
    if (not isinstance(board, np.ndarray) or 
        not isinstance(board[element_row, element_col], np.bool_)): 
        raise ValueError('board must be 2d boolean numpy array')
    elif (element_row == 0 or element_row == board.shape[0] - 1 or # row/col cannot be on borders
          element_col == 0 or element_col == board.shape[0] - 1): 
        raise ValueError('board elements must be in playable area')
    
    neighbors = []
    for row in range(-1, 2): 
        for col in range(-1, 2):
            if [row, col] == [0, 0]:
                continue
            else:
                neighbors.append(board[row+element_row, col+element_col])
    return neighbors


def update(board):
    """Returns a new game board with the updated state of the current state of the board."""
    size = board.shape[0] #size of board will be +2 of playable area
    new_board = np.full((size, size), False)

    for row in range(1, size - 1): #thus we subtract 1 instead of adding
        for col in range(1, size - 1):
            count = inspect(board, row, col).count(True) 
            if board[row, col]: 
                if count == 2 or count == 3: 
                    new_board[row, col] = True
            else:
                if count == 3: 
                    new_board[row, col] = True 
    return new_board


def get(board):
    """Get the co-ordinates of each living cell in a tick."""
    living = []

    for row in range(1, board.shape[0] - 1):
        for col in range(1, board.shape[0] - 1):
            if board[row, col]:
                living.append([row, col])
    return living


def get_3d(board, depth):
    """Get x, y and z of each living cell in each tick."""
    living_3d = [] #empty 3d-value (x, y, z) list

    for level in range(depth):
        sub_living = get(board) #2 dimensional sublist of current_state living cells
        for cell in sub_living:
            cell.append(level) 
        living_3d.append(sub_living)
        board = update(board)
    return living_3d


def get_xyz(board, depth):
    """Get XYZ coordinates - returns a tuple of seperated x, y, z lists."""
    living_3d = get_3d(board, depth) #gets ([x], [y], [z]) lists to depth number of ticks from start state
    x = []
    y = []
    z = []

    for level in range(depth):
        for element in living_3d[level]:
            a, b, c = element #a:x, b:y, c:z
            x.append(a)
            y.append(b)
            z.append(c)
    return x, y, z


class Plotter:
    """
    Defines matplotlib plots to show animation and 3d scatter plot.

    Attributes: 
    start_state - 2d boolean numpy array: The user-defined start state of the
    game board from which the game will run.
    """
    def __init__(self, start_state):
        self.current_state = start_state

    def update_2d(self):
        """Update the current state to the next tick."""
        self.current_state = update(self.current_state)
    
    def update_ani(self, frame, img): #frame is necessary for matplotlibs FuncAnimation method
        """
        Updates numpy array to a new plot 'img'.

        frame argument is necessary for matplotlibs FuncAnimation method
        returns img, - img needs to be a tuple, the comma signifies this
        """
        self.update_2d() 
        img.set_array(self.current_state) 
        return img,

    def animate(self, speed):
        """
        Creates animation by updating current_state and mapping it
        to 'img'.

        Arguments in FuncAnimation are passed through fargs, frames is implicit
        frames argument simply needs to be more than 1 to work, I don't know why
        """
        fig, ax = plt.subplots()
        img = plt.imshow(self.current_state)
        plt.axis('off') #hide labels
        animation = ani.FuncAnimation(fig, self.update_ani,
                                      fargs=(img,),
                                      frames=2,
                                      interval=speed) #animation variable is to appease matplotlib
        plt.show() 

    def show_3d(self, x, y, z, size):
        """
        Shows 3D scatter plot
        
        x, y, and z are derived from get_xyz(start_state, depth)
        size is determined in the UI based on the depth of the scatter plot
        """
        fig = plt.figure() 
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c='black', marker='s',
                             s=size)
        plt.show()


class Application(tk.Frame):
    """
    UI - User defined starting state of board with plotting options.

    A canvas with a grid drawn in is the main element,
    below that there is an 'Animate' and 'Plot 3D' Buttons.

    Two drop down menus for 'Speed' (of animation) and
    'Depth' (of 3D scatter plot).
    
    Another two buttons to set the depth and speed.
    """
    def __init__(self, root):
        """
        Initialization of UI element.

        grid_size (int): cells which make up the grid
        cell_size (int): size of cells in physical size
        depth (int): depth of 3D plot
        scatter_size (int): size of points on 3D plot
        speed (int): speed of animation

        game_board (2d bool_ numpy array): starts out as a completely False board based on grid size
        I'm adding +2 to each of rows and cols to give a buffer for the inspect() function to work properly
        """
        self.root = root

        self.grid_size = 50
        self.cell_size = 10
        self.depth = 25
        self.scatter_size = 60
        self.speed = 25

        self.create_grid()
        self.animate_button()
        self.plot3d_button()
        self.speed_dropdown()
        self.depth_dropdown()

        self.game_board = np.full((self.grid_size + 2, self.grid_size + 2), False)

    def create_grid(self): 
        """This is a canvas object within the grid() of tkinter.

        Using grid_size * cell_size to get the width/height of the window to make the canvas 
        big enough.

        Create rectangles to represent each element in the playable area of the game_board.

        Bind canvas to click event.
        """
        self.canvas = tk.Canvas(self.root, 
                                width=(self.grid_size * self.cell_size),
                                height=(self.grid_size * self.cell_size))
        self.canvas.pack() 
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = row * self.cell_size 
                y1 = col * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1,y1,x2,y2, 
                                             fill='white')

        self.canvas.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        """
        Click Event (Canvas element)

        Gets the x/y coordinates of the click event, then 
        changes the corresponding element in the game_board.

        Change the fill color of canvas() element based on state of game_board
        """
        x, y = event.x, event.y 
        grid_x = x // self.cell_size 
        grid_y = y // self.cell_size

        #check if indices are within bounds
        if (0 <= grid_x < self.grid_size 
            and 0 <= grid_y < self.grid_size):
            self.game_board[grid_y, grid_x] = not self.game_board[grid_y, grid_x] #tkinter and numpy disagree on x and y

            item_id = self.canvas.find_closest(x, y) #get coordinate of element in array

            fill_color = ('black' if
                          self.game_board[grid_y, grid_x]
                          else 'white')

            self.canvas.itemconfig(item_id, fill=fill_color)

    def animate_button(self):
        self.ani_button = tk.Button(self.root, 
                                    text='Animate', 
                                    command=self.on_animate_click)
        self.ani_button.pack(side='left', padx=10)

    def on_animate_click(self):
        plotter = Plotter(self.game_board)
        plotter.animate(self.speed)

    def plot3d_button(self):
        self.plot_button = tk.Button(self.root,
                                     text='Plot 3D',
                                     command=self.on_plot3d_click)
        self.plot_button.pack(side='left', padx=10)

    def on_plot3d_click(self):
        game_3d = self.game_board
        x, y, z = get_xyz(game_3d, self.depth)
        plotter = Plotter(self.game_board)
        plotter.show_3d(x, y, z, self.scatter_size)

    def speed_dropdown(self):
        self.selected_speed = tk.StringVar(self.root)
        self.selected_speed.set('Fast')

        self.speed_dropdown = tk.OptionMenu(self.root, 
                                            self.selected_speed, 
                                            'Fast', 'Gallop', 'Slow')
        self.speed_dropdown.pack(side='left', padx=10)

        self.speed_button = tk.Button(self.root, 
                                text='Set Speed',
                                command=self.set_speed)
        self.speed_button.pack(side='left', padx=self.cell_size)

    def set_speed(self):
        selected_speed = self.selected_speed.get()
        speed_dict = {'Fast': 25, 
                      'Gallop': 250, 
                      'Slow': 1000}
        self.speed = speed_dict[selected_speed]

    def depth_dropdown(self):
        self.selected_depth = tk.StringVar(self.root)
        self.selected_depth.set('Shallow')

        self.depth_button = tk.Button(self.root, 
                                text='Set Depth',
                                command=self.set_depth)
        self.depth_button.pack(side='right', padx=10)

        self.depth_dropdown = tk.OptionMenu(self.root, 
                                            self.selected_depth, 
                                            'Shallow', 'Mid', 'Deep')
        self.depth_dropdown.pack(side='right', padx=10)

    def set_depth(self):
        selected_depth = self.selected_depth.get()

        #index 0: depth of plot, index 1: size of scatter point
        depth_dict = {'Shallow': [25, 60], 
                      'Mid': [75, 5], 
                      'Deep': [225, 1]} 
        self.depth, self.scatter_size = depth_dict[selected_depth]


def main():
    root = tk.Tk()
    root.title('Conway\'s Game of Life')
    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()