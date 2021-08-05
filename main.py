from saturnin import Saturnin

if __name__ == "__main__":

	ROUND = int(raw_input("Input the target round number: "))
	while not (ROUND > 0):
		print "Input a round number greater than 0."
		ROUND = int(raw_input("Input the target round number again: "))

	ACTIVEBITS = int(raw_input("Input the number of acitvebits: "))
	while not (ACTIVEBITS < 256 and ACTIVEBITS > 0):
		print "Input the number of activebits:"
		ACTIVEBITS = int(raw_input("Input the number of acitvebits again: "))

	saturnin = Saturnin(ROUND, ACTIVEBITS)

	#saturnin.MakeModel()

	saturnin.SolveModel()
