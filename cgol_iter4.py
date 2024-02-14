#4th time around.
#something wrong with the previous algorithm, re: edges column wise,
#probably row wise as well, but i hadn't tested it out
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as ani
import tkinter as tk

class Board:
	def __init__(self, start_state):
		self.current_state = np.array(start_state, dtype='bool')
		self.rows, self.cols = self.current_state.shape

	def make(self, length=None, height=None):
		if length == None and height == None:
			length, height = [self.rows, self.cols]
		return np.full((length, height), False)

	def cell_pos(self, r, c):
		#determines the bounds of the box around the element we are inspecting
		#if it is at the beginning the box will go from 0,0 to 1,1
		#if it as the end, the box will go from -1,-1 to 0,0
		#top and bottom row and left and right column will also be considered edges
		#all center cells will have cells -1,-1 to 1,1 considered
		if r == 0 and c == 0: # start of grid 0,0
			r1 = 0
			c1 = 0
		elif r == 0 and c != 0: #top row 0, _
			r1 = 0
			c1 = -1
		elif c == 0 and r != 0: #left column, _, 0
			r1 = -1
			c1 = 0
		elif c != 0 and r != 0: #rest of grid _, _
			r1 = -1
			c1 = -1
		if r != self.rows - 1 and c != self.cols - 1: #rest of grid _, _ lol
			r2 = 2
			c2 = 2
		elif r == self.rows - 1 and c != self.cols - 1: #last row max, _
			r2 = 1
			c2 = 2
		elif c == self.cols - 1 and r != self.rows - 1: #last column _, max
			r2 = 2
			c2 = 1
		elif r == self.rows - 1 and c == self.cols - 1: #last cell max, max
			r2 = 1
			c2 = 1
		return [r1, r2, c1, c2]

	def inspect_element(self, r, c): #r, c are row, col indices of element
		r1, r2, c1, c2 = self.cell_pos(r, c)
		neighbors = []
		for row in range(r1, r2):
			for col in range(c1, c2):
				if [row, col] == [0,0]:
					continue
				else:
					neighbors.append(self.current_state[row+r, col+c])
		return neighbors

	def update_board(self):
		new_board = self.make()
		for row in range(self.rows):
			for col in range(self.cols):
				count = self.inspect_element(row, col).count(True)
				if self.current_state[row, col] == True:
					if count == 2 or count == 3:
						new_board[row, col] = True
				else:
					if count == 3:
						new_board[row, col] = True
		return new_board

	def update_2d(self):
		self.current_state = self.update_board()

class Visualizer:
	def __init__(self, state, frames):
		self.current_state = Board(state)
		self.animation_length = frames

	@staticmethod
	def update(frame, img, game):
		game.update_2d()
		img.set_array(game.current_state)
		return img,

	def animate(self):
		game = self.current_state
		fig, ax = plt.subplots()
		img = plt.imshow(game.current_state)
		plt.axis("off")
		animation = ani.FuncAnimation(fig, self.update, fargs=(img, game),
					frames=self.animation_length, interval=200)
		plt.show()

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()

		#grid and cell dims
		self.grid_width = 50
		self.grid_height = 50
		self.cell_width = 10
		self.cell_height = 10

		#instantiate window
		self.canvas = tk.Canvas(root, width=600, height=500)
		self.canvas.grid(row=0, column=0)

		self.create_grid()
		self.start_button()

		self.game_board = Board(np.zeros((self.grid_width, self.grid_height), dtype=bool))

	def create_grid(self):
		for row in range(self.grid_width):
			for col in range(self.grid_height):
				x1 = row * self.cell_width
				y1 = col * self.cell_height
				x2 = x1 + self.cell_width
				y2 = y1 + self.cell_height
				self.canvas.create_rectangle(x1,y1,x2,y2, fill='white')

		self.canvas.bind("<Button-1>", self.on_click)

	def on_click(self, event):
		x, y = event.x, event.y
		grid_x = x // self.cell_width
		grid_y = y // self.cell_height

		# Check if indices are within bounds
		if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
			self.game_board.current_state[grid_x, grid_y] = not self.game_board.current_state[grid_x, grid_y]

			# Get the item ID of the rectangle at the clicked position
			item_id = self.canvas.find_closest(x, y)

			# Change the fill color based on the updated state
			fill_color = 'black' if self.game_board.current_state[grid_x, grid_y] else 'white'

			# Update the fill color of the existing rectangle
			self.canvas.itemconfig(item_id, fill=fill_color)

	def start_button(self):
		# Create a rectangle for the button
		self.button_rect = self.canvas.create_rectangle(525, 237, 575, 263, fill='lightblue')

		# Create text inside the button
		button_text = "Start"
		text_x = (520 + 575) // 2
		text_y = 230
		self.button_text = self.canvas.create_text(text_x, text_y, text=button_text, fill='black', font=('Arial', 10))

		# Bind the button to the click event
		self.canvas.tag_bind(self.button_rect, '<Button-1>', self.on_button_click)

	def on_button_click(self, event):
		# Create an instance of Visualizer and call its animate method
		visualizer = Visualizer(self.game_board.current_state, frames=20)
		visualizer.animate()


if __name__ == '__main__':
	root = tk.Tk()
	app = Application(master=root)
	app.mainloop()
