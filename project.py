#Final Project for CS50P edx
#I have written this originally to contain a class "Board"
#but re-writing it without to satisfy the 3 functions condition
#of cs50 submit
#Firstly, a Board object was a 2d boolean numpy array
#with an init for start_state, which would have been the
#Board with some True elements
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk

#Function 1: Inspect Element - returns a list of neighboring elements
def inspect(board, r, c): #get a list of neighboring elements
    if (isinstance(board, np.ndarray) == False or #is board a numpy array?
        isinstance(board[r, c], np.bool_) == False): # is the board element a numpy boolean?
        raise ValueError('board must be 2d boolean numpy array')
    elif (r == 0 or r == board.shape[0] - 1 or # row cannot be on borders
          c == 0 or c == board.shape[0] - 1): #column likewise
        raise ValueError('board elements must be in playable area')
    neighbors = []
    for row in range(-1, 2): #from -1 to 1
        for col in range(-1, 2): # from -1 to 1
            if [row, col] == [0, 0]: #center
                continue #do not write the element we are inspecting
            else:
                neighbors.append(board[row+r, col+c])
    return neighbors

#Function 2: Update Board - returns a new game board with the updated state of the current state of the board
def update(board): #create a new board with the next tick of the current state
    size = board.shape[0] #size of board will be +2 of playable area
    new_board = np.full((size, size), False)
    for row in range(1, size - 1): #thus we subtract 1 instead of adding
        for col in range(1, size - 1):
            count = inspect(board, row, col).count(True) #number of True elements neighboring
            if board[row, col] == True: #if the element we are inspecting is alive
                if count == 2 or count == 3: #and it meets the criteria to keep living
                    new_board[row, col] = True #we must change the new_board to reflect that
            else:
                if count == 3: #since all elements on the new_board start dead
                    new_board[row, col] = True #we need only concern ourselves with any living elements on the new_board
    return new_board


def get(board): #get the co-ordinates of each living cell in a tick
    living = []
    for row in range(1, board.shape[0] - 1):
        for col in range(1, board.shape[0] - 1):
            if board[row, col] == True:
                living.append([row, col])
    return living


def get_3d(board, depth): #get x, y and z of each living cell in each tick
    living_3d = [] #empty 3d-value (x, y, z) list
    for level in range(depth):
        sub_living = get(board) #2 dimensional sublist of current_state living cells
        for cell in sub_living:
            cell.append(level) 
        living_3d.append(sub_living) #adding the modified self.get() list to the master list
        board = update(board) #updating the current_state of the board
    return living_3d

#Function 3: Get XYZ coordinates - returns a tuple of seperated x, y, z lists
def get_xyz(board, depth): #separate get_3d list into 3 seperate lists, one for each of x, y and z
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
    #Instantiate a Plotter object with the starting state of the board
    def __init__(self, start_state):
        self.current_state = start_state #start_state must be 2d boolean numpy array

    def update_2d(self): #update the current state to the next tick
        self.current_state = update(self.current_state)
    
    def update_ani(self, frame, img): #frame is necessary for matplotlibs FuncAnimation method
        self.update_2d() #changes the current_state
        img.set_array(self.current_state) #set new state array
        return img, #img needs to be a tuple, the comma signifies this

    def animate(self, speed):
        fig, ax = plt.subplots() #set subplots to figures and axes
        img = plt.imshow(self.current_state) #make a binary image of the games current state
        plt.axis('off') #hide labels
        animation = ani.FuncAnimation(fig, self.update_ani, #arguments for update_ani provided in fargs
                                      fargs=(img,), #frame is taken by FuncAnimation, so no need to call it
                                      frames=25, #the frames argument simply needs to be more than 1 to work, i dont know why. 
                                      interval=speed)
        plt.show() 

    def show_3d(self, x, y, z, size):
        fig = plt.figure() #set new figure
        ax = fig.add_subplot(111, projection='3d') #add new 3d subplot
        scatter = ax.scatter(x, y, z, c='black', marker='s', #x, y, z taken from get_xyz()
                             s=size) #size is determined by Depth
        plt.show()


class Application(tk.Frame):
    def __init__(self, root):
        self.root = root

        #grid and cell dimensions
        self.grid_size = 50 #cells that make up the the grid
        self.cell_size = 10 #cell size
        self.depth = 25 #depth of 3d plot
        self.scatter_size = 60 #size of 3d scatter point
        self.speed = 25 #speed of animation

        #calling GUI elements
        self.create_grid()
        self.animate_button()
        self.plot3d_button()
        self.speed_dropdown()
        self.depth_dropdown()

        #creating a boolean, square, 2d numpy array, all False
        #adding +2 to each of rows and cols to give buffer for inspect() function
        self.game_board = np.full((self.grid_size + 2, self.grid_size + 2), False)

    def create_grid(self): #this is a canvas object within the grid() of tkinter
        self.canvas = tk.Canvas(self.root, 
                                width=(self.grid_size * self.cell_size),  #we need to make the window big enough to handle the grid
                                height=(self.grid_size * self.cell_size))
        self.canvas.pack() 

        #draw grid          
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = row * self.cell_size #these give the coordinates for the start  
                y1 = col * self.cell_size #and end coordinates of the square representing an element
                x2 = x1 + self.cell_size #in the numpy array
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1,y1,x2,y2, 
                                             fill='white') #all white board is blank

        self.canvas.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        x, y = event.x, event.y #get x and y coordinates of click event
        grid_x = x // self.cell_size #get coordinate of element in grid
        grid_y = y // self.cell_size

        #check if indices are within bounds
        if (0 <= grid_x < self.grid_size 
            and 0 <= grid_y < self.grid_size):
            self.game_board[grid_y, grid_x] = not self.game_board[grid_y, grid_x] #for some reason tkinter and numpy disagree on what x and y mean

            #get item ID of the square at the clicked position
            item_id = self.canvas.find_closest(x, y) #get coordinate of element in array

            #change fill color based on state
            fill_color = ('black' if #black cells are living element in array
                          self.game_board[grid_y, grid_x] #just a continuation of the tkinter-numpy dispute
                          else 'white')

            #update fill color of existing square
            self.canvas.itemconfig(item_id, fill=fill_color)

    def animate_button(self):
        self.ani_button = tk.Button(self.root, 
                                    text='Animate', 
                                    command=self.on_animate_click)
        self.ani_button.pack(side='left', padx=10)

    def on_animate_click(self):
        plotter = Plotter(self.game_board)
        animate = plotter.animate(self.speed) #set variable just to appease matplotlib

    def plot3d_button(self):
        self.plot_button = tk.Button(self.root,
                                     text='Plot 3D',
                                     command=self.on_plot3d_click)
        self.plot_button.pack(side='left', padx=10)

    def on_plot3d_click(self):
        game_3d = self.game_board
        x, y, z = get_xyz(game_3d, self.depth)
        plotter = Plotter(self.game_board)
        plot3d = plotter.show_3d(x, y, z, self.scatter_size)

    def speed_dropdown(self):
        self.selected_speed = tk.StringVar(self.root)
        self.selected_speed.set('Fast') # Default Speed

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
        speed_dict = {'Fast': 25, 'Gallop': 250, 'Slow': 1000}
        self.speed = speed_dict[selected_speed]

    def depth_dropdown(self):
        self.selected_depth = tk.StringVar(self.root)
        self.selected_depth.set('Shallow') # Default Depth

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
        depth_dict = {'Shallow': [25, 60], 'Mid': [75, 5], 'Deep': [225, 1]} #index 0: depth of plot, index 1: size of scatter point
        self.depth, self.scatter_size = depth_dict[selected_depth]


def main():
    root = tk.Tk()
    root.title('Conway\'s Game of Life')
    app = Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()