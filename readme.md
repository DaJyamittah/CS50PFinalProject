# Conway's Game of Life

### Video Demo:  [Youtube Demo](https://youtu.be/Aw1nAEB8Mx4)
#### Description: Conway's Game of Life with a very unsatisfying 3D twist!
    
#### Library Requirements:
* numpy
* matplotlib
* tkinter

#### Installation and running
First, it must be ensured that the correct libraries are set up on the system. In order to do this, open the command line interface and type
``` pip install ``` and then the libraries we need to install. For example to install numpy:
``` pip install numpy ```.

After all the required libraries are installed, change directories to where the file is saved, then ```python project.py``` and it ought to run. 

#### Conway's Game of Life
Conway's Game of Life is a [cellular automata](https://en.wikipedia.org/wiki/Cellular_automaton).
It follows a very simple set of rules which can make surprisingly complex shapes and exhibits some interesting behaviours.
The game board is a 2 dimensional grid. In this grid, each element can have one of two states: Alive or Dead. 
The rules are as follows: 
* If a living element has two or three neighbors, then it will continue living to the next iteration of the game
* If a living element has less than two or more than three neighbors, it will perish from under- or over- population.
* If a dead element has exactly three neighbors, it will come to life.

This is the basis for this program.

---
#### A screen grab of an animation mid-way

![Animation](https://i.ibb.co/8Xq3Vcj/cs50finalproject-animation.png 'Animation')

#### Code Structure
There are three main functions which deal with the actual data of the game, then 2 classes which deal with the visualization and user interface.

The first function is ```inspect_element(board, r, c)```. 

This takes a 2 dimensional boolean numpy array as a 'board' argument, and the row/column position of the element we want to inspect. This function returns a list of the neighboring elements in a square. This was a function which gave me a lot of headache because while it works great in the center of the board, there were range issues when it came to inspecting elements on the borders of the board. This is because I used a nested for loop to iterate through the row/column co-ordinates from -1 to 1 to get the surrounding elements captured in a list. After a lot of trial and error, and a lot of very ugly code, I decided the simplest fix was to simply add a border around the game board which did not get inspected. 

It's a complete hack but it works, so I kept it.

The second function is ```update(board)```. This function has the same criteria for the 'board' argument as above. Using the inspect_element function on every element in the playable area. The playable area is the square 2d numpy array minus the border rows and columns. It determines the state of each cell in the grid then returns a new array for the next state of the board.

The third function is ```get_xyz(board, depth)```. This function gets a list for each of the x, y and z co-ordinates. The x and y co-ordinates are simple enough - they represent the row/column indices of the living elements in a game board. the z element represents the number of ticks passed since the starting state of the board. Not only did I want to provide an animation of the Conway's cellular automata, but a 3d snapshot of any starting state and how it would progress. The reason for having the x, y and z co-ordinates stored in seperate lists is because matplotlibs 3d scatter plots takes the arguments for the points in that way.

---
##### Plotter Class
The Plotter class is initialized with a start_state, this is the game board we have been dealing with so far (2d boolean numpy array). This is used as a sort of jumping off point from which the simulation can launch from. 

There are two main methods for this class: ```animate(self, speed)``` and ```show_3d(self, x, y, z, size)```.

The current_state is set to be start_state to begin, but then the update() function is used to set the current_state to be the new tick - it is in this way the animation moves forward tick by tick. 

I decided not to show the animation and the 3d plot at the same time because my computer was barely able to produce the 3d plots on it's own. I am not sure if it is due to a highly inefficient program or if it is just my potato laptop.

The ```animate(self, speed)``` method takes a 'speed' argument from the UI drop down. The 'frames' argument for FuncAnimation, I thought, would determine the length of the animation, but found that as long as it is higher than 1 it will continue the animation to it's logical end, if it is set to 1 it will show only one tick after the start_state, if it is set to 0 it only shows the start_state. I'm not entirely sure why, but have a suspicion it is due to not tracking the frames as they progress, instead just updating the current_state.

The ```show_3d(self, x, y, z, size)``` method takes the x, y, and z coordinates from the get_xyz() function and the size argument comes from the drop down menu (depending on what 'depth' the user picks). I decided to keep the labels because they 'somewhat' provide a sense of scale. At some point in the future, I would like to make the 3d scatter plot itself look nicer, or maybe find some alternative 3d plot that would look better. I was looking for a way to get the bitmap image, like voxels instead of pixels, but I could find no such solution, and could not be bothered to make that solution myself, so I decided to just use the 3d scatter plots and set the markers to little blocks. 

---
#### Application Class
This is the User Interface. This is where the grid and game are initially all set up. To start - an empty game_board is made with np.full().
Though this is the longest class, there is not much to explain here. I have set the grid size, cell size and the plot/animation variables in the initialization. The initial grid start out all white and when any square is clicked that square changes and the game_board also changes according to the x/y coordinates of the click event.

![Main Menu](https://i.ibb.co/jDhBjyG/cs50finalproject-main.png 'Main Menu')

At the bottom of the grid there are a few options. The first two are simply to plot the current grid. The 'speed' drop down affects only the animation, and has 3 settings the user can choose, from slow to fast. The 'depth' drop down only affects the 3d plot and also has 3 settings, which go from 'shallow' to 'deep', this affects the number of ticks the 3d plot will show past it's origin, as well as the marker size, as I found the large sizes that were suitable for a depth of 25 made a blob-like plot at a depth of 225.

After changing the drop-down menu item, the 'set' button next to the drop down should be clicked before changes take effect to the respective variables.

![3D Plot](https://i.ibb.co/9w5nwt6/cs50finalproject-3d.png  '3D Plot')

---
That's all there is! Thanks for reading.











    