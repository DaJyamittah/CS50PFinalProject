import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk

class Board:
    #Initializing a Board object will create an empty Board, a square with 'size' width and length
    def __init__(self, size):
        self.size = size #specifies size of square 2d array
        self.current_state = self.make() #empty playing board
        self.play_area = range(1, size + 1) #the playable area, discounting the border rows and columns

    def make(self): #make empty array
        return np.full((self.size + 2, self.size + 2), False) #adds a border around for calculating neighboring elements

    def inspect(self, r, c): #get a list of the neighboring elements of a co-ordinate
        neighbors = []
        for row in range(-1, 2): # from -1 to 1
            for col in range(-1, 2):# from -1 to 1
                if [row, col] == [0, 0]: #center 
                    continue
                else:
                    neighbors.append(self.current_state[row+r, col+c])
        return neighbors

    def update(self): #next tick of current_state
        new_board = self.make() #all dead board
        for row in self.play_area:
            for col in self.play_area:
                count = self.inspect(row, col).count(True) #number of living cells neighboring element
                if self.current_state[row, col] == True: #if the element we are inspecting is living
                    if count == 2 or count == 3: #and it meets the survival criteria
                        new_board[row, col] = True #we must change the new_board to reflect that
                else:
                    if count == 3: #since all elements on the new_board start dead, we don't need to change anything if it flips to dead
                        new_board[row, col] = True #but if it is to be alive in the next tick of the game, we should update the new_board 
        return new_board

    def update_2d(self): #2d snapshot of the games state
        self.current_state = self.update()

    def get(self): #get the co-ordinates of each living cell in a tick
        living = []
        for row in self.play_area:
            for col in self.play_area:
                if self.current_state[row, col] == True:
                    living.append([row, col])
        return living
    
    def get_3d(self, depth): #get x, y and z of each living cell in each tick
        living_3d = [] #empty 3d list
        for level in range(depth):
            sub_living = self.get() #2 dimensional sublist of current_state living cells
            for cell in sub_living:
                cell.append(level) 
            living_3d.append(sub_living) #adding the modified self.get() list to the master list
            self.update_2d() #updating the current_state of the board
        return living_3d
    
    def get_xyz(self, depth): #separate get_3d list into 3 seperate lists, one for each of x, y and z
        living_3d = self.get_3d(depth)
        x = []
        y = []
        z = []
        for level in range(depth):
            for element in living_3d[level]:
                a, b, c = element
                x.append(a)
                y.append(b)
                z.append(c)
        return x, y, z

class Plotter:
    #Instantiate a Plotter object with a non-empty Board object
    def __init__(self, start_state):
        self.current_state = start_state #start_state must be Board object

    @staticmethod
    def update(frame, img, game): #game is Board object
        game.update_2d()
        img.set_array(game.current_state) #set binary map
        return img,

    def animate(self, length):
        game = self.current_state
        fig, ax = plt.subplots() #set subplots to figures and axes
        img = plt.imshow(game.current_state) #make a binary image of the games current state
        plt.axis('off') #hide labels
        animation = ani.FuncAnimation(fig, self.update, 
                                      fargs=(img, game),
                                      frames=length, 
                                      interval=25)
        plt.show() 

    def show_3d(self, x, y, z):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(x, y, z, c='black', marker='s', 
                             s=25)
        plt.show()

class Application(tk.Frame):
    def __init__(self, root):
        self.root = root

        #grid and cell dimensions
        self.grid_size = 50 #cells that make up the the grid
        self.cell_size = 10 #cell size
        self.frames = 25 #length of animation/depth of 3d plot

        #calling GUI elements
        self.create_grid()
        self.animate_button()
        self.plot3d_button()

        #creating an empty Board object
        self.game_board = Board(self.grid_size)

    def create_grid(self):
        self.canvas = tk.Canvas(self.root, 
                                width=(self.grid_size * self.cell_size), 
                                height=(self.grid_size * self.cell_size))
        self.canvas.pack() 

        #draw grid          
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
        x, y = event.x, event.y
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size

        #check if indices are within bounds
        if (0 <= grid_x < self.grid_size 
            and 0 <= grid_y < self.grid_size):
            self.game_board.current_state[grid_y, grid_x] = not self.game_board.current_state[grid_y, grid_x] #for some reason tkinter and numpy disagree on what x and y mean

            #get item ID of the square at the clicked position
            item_id = self.canvas.find_closest(x, y)

            #change fill color based on state
            fill_color = ('black' if 
                          self.game_board.current_state[grid_y, grid_x] #just a continuation of the tkinter-numpy dispute
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
        animate = plotter.animate(self.frames)

    def plot3d_button(self):
        self.plot_button = tk.Button(self.root,
                                     text='Plot 3D',
                                     command=self.on_plot3d_click)
        self.plot_button.pack(side='left', padx=10)

    def on_plot3d_click(self):
        x, y, z = self.game_board.get_xyz(self.frames)
        plotter = Plotter(self.game_board)
        plot3d = plotter.show_3d(x, y, z)

def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == '__main__':
    main()