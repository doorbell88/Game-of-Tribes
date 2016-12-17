# Game of Life

from copy import deepcopy
from time import sleep, time
from subprocess import Popen, PIPE
from termcolor import colored, cprint
from random import randint, choice
import os



# get size of terminal
#width
stdout = Popen('tput cols', shell=True, stdout=PIPE).stdout
WIDTH = int( stdout.read() )
#height
stdout = Popen('tput lines', shell=True, stdout=PIPE).stdout
HEIGHT = int( stdout.read() ) - 1




##### CLASSES #####

# Display of the window
class Window(object):
	def __init__(self, border_color):
		self.border_color = border_color
		self.width = WIDTH
		self.height = HEIGHT
		self.size = (self.height * self.width)

		self.box = []
		self.previous = []
		self.next = []

		#create blank window box
		for y in range(self.height):
			self.box.append([" "] * self.width)


		#draw window border
		for y in range(0, self.height):
			for x in range(0, self.width):
				#top 
				self.box[0][x] = colored( "=", self.border_color )
				#bottom
				self.box[self.height - 1][x] = colored( "=", self.border_color )
				#left
				self.box[y][0] = colored( "|", self.border_color )
				#right
				self.box[y][self.width - 1] = colored( "|", self.border_color )

		# Make copies for iteration
		self.previous = deepcopy(self.box)
		self.next = deepcopy(self.box)


	# Print "previous" to the terminal
	def display(self):
		# Clear screen and scrollback buffer
		os.system("clear && printf '\e[3J' ")
		# os.system("clear")

		# print
		for row in range( len(self.previous) ):
			current_row = []
			for col in range( len(self.previous[row]) ):
				cell = self.previous[row][col]
				current_row.append( colored(cell, colors.get(cell, 'green')) )
			print "".join(current_row)
			


	# Refresh the previous and next boards
	def refresh(self):
		# Create template for next iteration
		self.previous = deepcopy(self.next)
		self.next = deepcopy(self.box)


	# Create randomized initial conditions
	def random(self, fraction):
		# Make a few random cells "on"
		n=0
		while n < (self.height * self.width)/fraction :
			y = randint(1, self.height-2)
			x = randint(1, self.width-2)
			self.previous[y][x] = '#'
			n += 1

	# Return the population of the map
	def Census(self, tribe):
		census = 0
		for y in range(1, self.height-1):
			for x in range(1, self.width-1):
				if self.previous[y][x] == tribe.symbol:
					census += 1
		return census




##################################################################
# Import Tribes
from TribeA import CellChecker, TribeA
from TribeB import CellChecker, TribeB
from TribeC import CellChecker, TribeC
# from TribeD import CellChecker, TribeD
##################################################################


Grid = Window('red')

T_A = TribeA('*', 'cyan')
T_B = TribeB('#', 'magenta')
T_C = TribeC('@', 'yellow')
# T_D = TribeC('*', 'white')

colors = 	{	T_A.symbol : T_A.color ,
				T_B.symbol : T_B.color ,
				T_C.symbol : T_C.color ,
				# T_D.symbol : T_C.color
			}


# Grid.random(2)

# T_A.random(Grid, 4, y_bounds=[1, Grid.height/2])
# T_B.random(Grid, 4, x_bounds=[1, Grid.width/2])
# T_C.random(Grid, 4, y_bounds=[Grid.height*1/3, Grid.height-2], x_bounds=[Grid.width*1/3, Grid.width-2])

T_A.random(Grid,8)
T_B.random(Grid,6)
T_C.random(Grid,4)

T_A.enemies = [T_B, T_C]
T_B.enemies = [T_C]
T_C.enemies = [T_A]

# Give preview of grid before starting
Grid.display()
sleep(1)


# Infinite Loop
turn = 1
while True:

	if turn%3 == 0:
		T_A.RunRules(Grid, T_A.Rules)					# Game of Life rules
		Grid.display()
		Grid.refresh()
		
	elif turn%3 == 1:
		T_B.RunRules(Grid, T_B.Rules)					# Game of Life rules
		Grid.display()
		Grid.refresh()

	elif turn%3 == 2:
		T_C.RunRules(Grid, T_C.Rules)					# Game of Life rules
		Grid.display()
		Grid.refresh()


	# sleep(0.01)
	turn += 1




