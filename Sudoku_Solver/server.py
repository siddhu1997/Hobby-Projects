import sys

try:

	from flask import Flask
	from flask_ngrok import run_with_ngrok

except Exception as e:
	print("Please install flask-ngrok before you can continue. Try: 'pip install flask-ngrok'")
	sys.exit(0)

try:
	from sudokuSolver import *

except Exception as e:
	print("sudokuSolver.py missing!")
	sys.exit(0)

array = sudokuSolver()
print("Initial Array:")
array.sprint()
array.solve()
print("\nSolution:")
array.sprint()
