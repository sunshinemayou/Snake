def output(number):
	fOutput = open("Score","w")
	fOutput.seek(0)
	fOutput.truncate()
	fOutput.write(str(number))