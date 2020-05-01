'''
Sudoku Solver using Backtracking Algorithm

'''


import sys

class sudokuSolver:

	def __init__(self):

		self._range_ = range(9)
		self._box_   = range(3)								#Constructor that return an empty 9x9 matrix

		self.matrix = [ [0 for x in self._range_] for y in self._range_ ]

	def Empty(self,rc_list):

		for row in self._range_:
			for column in self._range_:
				if self.matrix[row][column] == 0:
					rc_list[0] = row 
					rc_list[1] = column
					return True
		return False

	def inRow(self,row,number):
		
		if number in self.matrix[row]:
			return True
		else:
			return False

	def inColumn(self,column,number):

		for i in self._range_:
			if self.matrix[i][column] == number:
				return True
		return False

	def inBox(self,row,column,number):

		for i in self._box_:
			for j in self._box_:
				if self.matrix[i+row][j+column] == number:
					return True
		return False

	def isSafe(self,row,column,number):
		return not self.inRow(row,number) and not self.inColumn(column,number) and not self.inBox((row-(row%3)),(column-(column%3)),number)

	#Where the actual Backtracking Algorithm starts!

	def solve(self):
		
		rc_list = [0,0]

		#If there is no empty cell, means, solution complete.
		if not self.Empty(rc_list):
			return True

		row =    rc_list[0]
		column = rc_list[1]

		for number in range(1,10):

			if(self.isSafe(row,column,number)):
				self.matrix[row][column] = number

				if(self.solve()):
					return True

				self.matrix[row][column] = 0 
		return False

	def sprint(self):
		print()
		for row in self._range_:
			print(self.matrix[row])