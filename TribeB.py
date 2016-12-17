# GOL (Game of Life) Ruleset

from random import randint, choice

# A spider that performs operations on the whole board
class CellChecker(object):
	def __init__(self):
		pass

	# Count how many neighboring cells (within margin) are a certain symbol
	def CountNeighbors(self, board, position, margin):
		self.position = position

		neighbors = {}
		# neighbors = 0
		for j in range(-margin, margin+1):
			for i in range(-margin, margin+1):

				# Do not check the current (center) cell
				if j==0 and i==0:
					pass

				else:
					y = self.position[0] + j
					x = self.position[1] + i

					# if going off the edge of the map, pass
					if 	y < 1 or 				\
						x < 1 or 				\
						y > board.height-1 or 	\
						x > board.width-1:
							pass
					else:
						if board.previous[y][x] not in neighbors:
							neighbors[ board.previous[y][x] ] = 0
						neighbors[ board.previous[y][x] ] += 1

		return neighbors

	# Create randomized initial conditions
	def random(self, board, fraction, **kwargs):
		# Make a few random cells "on"
		y_bounds = kwargs.get('y_bounds', [1, board.height-2])
		x_bounds = kwargs.get('x_bounds', [1, board.width-2])
		n=0
		while n < ((y_bounds[1]-y_bounds[0]) * (x_bounds[1]-x_bounds[0]))/fraction :
			y = randint(y_bounds[0], y_bounds[1])
			x = randint(x_bounds[0], x_bounds[1])
			board.previous[y][x] = self.symbol
			n += 1

	# Randomly move some random alive cells
	def RandomMigration(self, board):
		for y in range(1, board.height-1):
			for x in range(1, board.width-1):
				if randint(1,50) == 1:
					j = choice([-1, 1])
					i = choice([-1, 1])

					# if previous spot is occupied
					if board.previous[y][x] == '#':
						# if adjacent spot is unoccupied
						if board.next[y+j][x+i] == ' ':

							# move to unoccupied spot
							if randint(1,2) == 1:
								board.previous[y][x] = ' '
							board.next[y+j][x+i] = '#'

	# Enforce GOL rules
	def RunRules(self, board, rules):
		for y in range(1, board.height-1):
			for x in range(1, board.width-1):
				rules(board, [y,x])



###############################################################################################
# TribeB Rules
class TribeB(CellChecker):
	def __init__(self, symbol, color):
		CellChecker.__init__(self)
		self.symbol = symbol
		self.color = color


	def Rules(self, board, position):
		self.position = position	#[y,x]
		self.board = board
		y = self.position[0]
		x = self.position[1]
		margin = 2					# Number of cells around self a cell is aware of
		friend = self.symbol
		enemies = self.enemies
		enemy_symbols = []

		neighbors = self.CountNeighbors(board, position, margin)
		alive_neighbors = neighbors.get(friend, 0)
		
		alive_enemies = 0
		for enemy in self.enemies:
			alive_enemies += neighbors.get(enemy.symbol, 0)
			enemy_symbols.append(enemy.symbol)


		###############################################################################################
		# TribeB -- Rules
		###############################################################################################

		
		# Any live cell with 6-10 live neighbors lives on to the next generation
		if board.previous[y][x] == self.symbol:					# Previously alive
			# if 6 <= alive_neighbors <= 10:
			if 6 <= alive_neighbors <= 10:
				board.next[y][x] = self.symbol
				return True

		# Any dead cell with 8-9 live neighbors becomes a live cell, as if by reproduction
		elif board.previous[y][x] != self.symbol:				# Previously dead or enemy
			# if 8 <= alive_neighbors <= 9:
			if 8 <= alive_neighbors <= 9:
				board.next[y][x] = self.symbol
				return True
			else:
				board.next[y][x] = board.previous[y][x]
				return False


		# # Any live cell with fewer than 6 live neighbors dies, as if caused by underpopulation
		# # Any live cell with more than 10 live neighbors dies, as if by overpopulation
		# else:
		# 	board.next[y][x] = board.previous[y][x]								# Under/Overpopulation
		# 	return False


		# ENEMY EATING
		# If enough enemies are neighboring, begin to eat them
		if board.previous[y][x] == self.symbol:
			# if 6 <= alive_enemies <= 18:

			number_to_eat = 0
			if alive_enemies >= 5:
				number_to_eat = alive_enemies/3

				eat=0
				while eat < number_to_eat:
					n=0
					j=0
					i=0
					# while board.next[y+j][x+i] != self.symbol and n<((margin*2)**2):
					while board.next[y+j][x+i] not in self.enemies and n<(margin*3):
						j = randint(-1,1)
						i = randint(-1,1)
						n+=1
						if 	(y+j) > 2 and (x+i) > 2 and \
							(y+j) < board.height-2 and (x+i) < board.width-2:
								board.next[y+j][x+i] = self.symbol
					eat += 1



		###############################################################################################


