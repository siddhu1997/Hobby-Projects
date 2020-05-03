import sys
import os

try:

	from flask import Flask, request, render_template
	from flask_ngrok import run_with_ngrok

except Exception as e:
	print("Please install flask-ngrok before you can continue. Try: 'pip install flask-ngrok'")
	sys.exit(0)

try:
	from sudokuSolver import *

except Exception as e:
	print("sudokuSolver.py missing!")
	sys.exit(0)

def extractInput(raw_input_data):
	ipData = {x.split(">")[0].strip():int(x.split(">")[1].strip()) for x in raw_input_data.split(" ")}
	return ipData

def packOutput(output_matrix):
	opData = []
	for row in output_matrix:
		opData.append(",".join([str(x) for x in row]))
	opData = ", ".join(opData)
	opData = "[ " + opData + " ]"
	return opData

app = Flask(__name__, static_url_path='', static_folder=(os.getcwd()+'/public'))
run_with_ngrok(app)

@app.route('/', methods=['GET','POST'])
def index():
	if(request.method == "POST"):
		INPUT_DATA = request.form.get("INPUTDATA")
		INPUT_DATA.strip()
		if(INPUT_DATA == None or INPUT_DATA==''):
			return "{\"error\" : \"1\", \"message\" : [\"No Input Found\"], \"ans\" : []}"
		else:
			try:
				input_dictionary = extractInput(INPUT_DATA)
			except Exception as e:
				return "{\"error\" : \"1\", \"message\" : [\"Invalid Input!...\"], \"ans\" : []}"
			array = sudokuSolver(input_dictionary)
			error_status, msg = array.checkError()
			if error_status == True:
				return "{\"error\" : \"1\", \"message\" : "+str(msg)+", \"ans\" : []}"
			else:
				array.solve()
				answer = packOutput(array.outputMatrix())
				return "{\"error\" : \"0\", \"message\" : [\"Success\"], \"ans\" : "+str(answer)+"}"
	else:
		return render_template('index.html')

if __name__ == '__main__':
	app.run()