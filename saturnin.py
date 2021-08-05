from gurobipy import *

import time
import os

class Saturnin:
	def __init__(self, Round, activebits):
		self.Round = Round
		self.activebits = activebits
		self.blocksize = 256
		self.filename_model = "Saturnin_" + str(self.Round) + "_" + str(self.activebits) + ".lp"
		self.filename_result = "result_" + str(self.Round) + "_" + str(self.activebits) + ".txt"
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()

	#Linear inequalities for the Saturnin Sbox
	S_T=[[[1, 1, 1, 4, -2, -2, -2, -2, 1],\
        [-2, -1, -5, -3, 2, -1, 1, 3, 7],\
        [1, 1, 4, 1, -2, -2, -2, -2, 1],\
        [-5, -3, -1, -2, -1, 3, 2, 1, 7],\
        [2, 0, 0, 0, -1, 0, -1, -1, 1],\
        [0, -1, -1, -2, 4, 3, 2, 3, 0],\
        [-2, 0, -1, 0, 3, -2, -1, -1, 4],\
        [1, 4, 1, 1, -2, -2, -2, -2, 1],\
        [-1, -2, -1, 0, 3, 3, 4, 2, 0]],\
	\
	[[1, 1, 4, 1, -2, -2, -2, -2, 1],\
        [-1, -2, -3, -5, -1, 3, 2, 1, 7],\
        [1, 1, 1, 4, -2, -2, -2, -2, 1],\
        [-5, -3, -1, -2, 2, -1, 1, 3, 7],\
        [1, 4, 1, 1, -2, -2, -2, -2, 1],\
        [-1, -2, -1, 0, 4, 3, 2, 3, 0],\
        [-2, -1, -5, -3, 1, 2, 3, -1, 7],\
        [-3, -5, -2, -1, 3, 1, -1, 2, 7],\
        [4, 1, 1, 1, -2, -2, -2, -2, 1],\
        [-1, 0, -1, -1, 2, 2, 3, 2, 0]]]
	NUMBER = 9

	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Minimize\n")
		eqn = []
		for i in range(0,64):
			for j in range(0,4):
				eqn.append("x" + "_" + str(self.Round) + "_" +str(i) + "_" + str(j))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	@staticmethod
	def CreateVariables(n,s):
		"""
		Generate the variables used in the model.
		"""
		array = [[" " for j in range(0,4)] for i in range(0,64)]
		for i in range(0,64):
			for j in range(0,4):
				array[i][j] = s + "_" + str(n) + "_" + str(i) + "_" + str(j)
		return array

	def ConstraintsByCopy(self, variablex, variableu, variabley):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_model,"a")
		for j in range(0,4):
			temp = []
			temp.append(variablex[j])
			temp.append(variableu[j])
			temp.append(variabley[j])
			s = " - ".join(temp)
			s += " = 0"
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()

	def ConstraintsByXor(self, variabley,variablev,variablex):
		"""
		Generate the constraints by Xor operation.
		"""
		fileobj = open(self.filename_model,"a")
		for j in range(0,4):
			temp = []
			temp.append(variablex[j])
			temp.append(variablev[j])
			temp.append(variabley[j])
			s = " - ".join(temp)
			s += " = 0"
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()
		
	def ConstraintsByAlfa(self, variablein, variableout, r, i, n):
		"""
		Generate the constraints by copy operation.
		"""
		fileobj = open(self.filename_model,"a")
		temp = []
		temp.append(variablein[1])
		temp.append(variableout[0])
		temp.append("t_"+str(r)+"_"+str(i)+"_"+str(n))
		s = " - ".join(temp)
		s += " = 0"
		fileobj.write(s)
		fileobj.write("\n")
                temp = []
		temp.append(variableout[3])
		temp.append(variablein[0])
		temp.append("t_"+str(r)+"_"+str(i)+"_"+str(n))
		s = " - ".join(temp)
		s += " = 0"
		fileobj.write(s)
		fileobj.write("\n")
		s = variablein[2] + " - " + variableout[1] + " = 0"
		fileobj.write(s)
		fileobj.write("\n")
		s = variablein[3] + " - " + variableout[2] + " = 0"
		fileobj.write(s)
		fileobj.write("\n")		
		fileobj.close()

	def ConstraintsByMDS(self, variable1, variable2, r):
                variableA = Saturnin.CreateVariables(r,"a")
                variableB = Saturnin.CreateVariables(r,"b")
                variableC = Saturnin.CreateVariables(r,"c")
                variableD = Saturnin.CreateVariables(r,"d")
                variableE = Saturnin.CreateVariables(r,"e")
                variableF = Saturnin.CreateVariables(r,"f")
                variableG = Saturnin.CreateVariables(r,"g")
                variableH = Saturnin.CreateVariables(r,"h")
                variableI = Saturnin.CreateVariables(r,"i")
                variableJ = Saturnin.CreateVariables(r,"j")
                for i in range(0,16):
                        self.ConstraintsByCopy(variable1[4*i +1],variableA[2*i],variableB[4*i +1])
                        self.ConstraintsByCopy(variable1[4*i +3],variableA[2*i +1],variableB[4*i +3])
                        self.ConstraintsByXor(variable1[4*i],variableA[2*i],variableB[4*i])
                        self.ConstraintsByXor(variable1[4*i +2],variableA[2*i +1],variableB[4*i +2])
                        self.ConstraintsByAlfa(variableB[4*i +1],variableC[2*i],r,i,0)
                        self.ConstraintsByAlfa(variableB[4*i +3],variableC[2*i +1],r,i,1)
                        self.ConstraintsByCopy(variableB[4*i],variableD[2*i],variableE[4*i])
                        self.ConstraintsByCopy(variableB[4*i +2],variableD[2*i +1],variableE[4*i +2])
                        self.ConstraintsByXor(variableC[2*i],variableD[2*i +1],variableE[4*i +1])
                        self.ConstraintsByXor(variableC[2*i +1],variableD[2*i],variableE[4*i +3])
                        self.ConstraintsByAlfa(variableE[4*i],variableF[2*i],r,i,2)
                        self.ConstraintsByAlfa(variableE[4*i +2],variableF[2*i +1],r,i,3)
                        self.ConstraintsByAlfa(variableF[2*i],variableG[2*i],r,i,4)
                        self.ConstraintsByAlfa(variableF[2*i +1],variableG[2*i +1],r,i,5)
                        self.ConstraintsByCopy(variableE[4*i +1],variableH[2*i],variableI[4*i +1])
                        self.ConstraintsByCopy(variableE[4*i +3],variableH[2*i +1],variableI[4*i +3])
                        self.ConstraintsByXor(variableG[2*i],variableH[2*i],variableI[4*i])
                        self.ConstraintsByXor(variableG[2*i +1],variableH[2*i +1],variableI[4*i+2])
                        self.ConstraintsByCopy(variableI[4*i],variableJ[2*i],variable2[4*i])
                        self.ConstraintsByCopy(variableI[4*i +2],variableJ[2*i +1],variable2[4*i +2])
                        self.ConstraintsByXor(variableI[4*i +1],variableJ[2*i +1],variable2[4*i +1])
                        self.ConstraintsByXor(variableI[4*i +3],variableJ[2*i],variable2[4*i +3])                                
                
	def ConstraintsBySbox(self, variable1, variable2):
		"""
		Generate the constraints by sbox layer.
		"""
		fileobj = open(self.filename_model,"a")
		for k in range(0,32):
			for coeff in Saturnin.S_T[0]:
				temp = []
				for u in range(0,4):
					temp.append(str(coeff[u]) + " " + variable1[2*k][3-u])
				for v in range(0,4):
					temp.append(str(coeff[v + 4]) + " " + variable2[2*k][3-v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coeff[Saturnin.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
			for coeff in Saturnin.S_T[1]:
				temp = []
				for u in range(0,4):
					temp.append(str(coeff[u]) + " " + variable1[2*k+1][3-u])
				for v in range(0,4):
					temp.append(str(coeff[v + 4]) + " " + variable2[2*k+1][3-v])
				temp1 = " + ".join(temp)
				temp1 = temp1.replace("+ -", "- ")
				s = str(-coeff[Saturnin.NUMBER - 1])
				s = s.replace("--", "")
				temp1 += " >= " + s
				fileobj.write(temp1)
				fileobj.write("\n")
		fileobj.close(); 

	@staticmethod

	def nibblePermut(variable,r):
		"""
		Linear layer of Saturnin.
		"""
		index1 = [0,13,10,7,4,1,14,11,8,5,2,15,12,9,6,3,
                         16,29,26,23,20,17,30,27,24,21,18,31,28,25,22,19,
                         32,45,42,39,36,33,46,43,40,37,34,47,44,41,38,35,
                         48,61,58,55,52,49,62,59,56,53,50,63,60,57,54,51]
		index3 = [0,49,34,19,4,53,38,23,8,57,42,27,12,61,46,31,
                         16,1,50,35,20,5,54,39,24,9,58,43,28,13,62,47,
                         32,17,2,51,36,21,6,55,40,25,10,59,44,29,14,63,
                         48,33,18,3,52,37,22,7,56,41,26,11,60,45,30,15]
		array = [[" " for i in range(0,4)] for j in range(0,64)]
		if r%4 == 1:
        		for i in range(0,64):
                                for j in range(0,4):
                                        array[i][j] = variable[index1[i]][j]
                elif r%4 == 3:
                        for i in range(0,64):
                                for j in range(0,4):
                                        array[i][j] = variable[index3[i]][j]
                else:
        		for i in range(0,64):
                                for j in range(0,4):
                                        array[i][j] = variable[i][j]                        
		return array

	def InvnibblePermut(variable,r):
		"""
		Linear layer of Saturnin.
		"""
		index1 = [0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11,
                          16,21,26,31,20,25,30,19,24,29,18,23,28,17,22,27,
                          32,37,42,47,36,41,46,35,40,45,34,39,44,33,38,43,
                          48,53,58,63,52,57,62,51,56,61,50,55,60,49,54,59]		
		index3 = [0,17,34,51,4,21,38,55,8,25,42,59,12,29,46,63,
                          16,33,50,3,20,37,54,7,24,41,58,11,28,45,62,15,
                          32,49,2,19,36,53,6,23,40,57,10,27,44,61,14,31,
                          48,1,18,35,52,5,22,39,56,9,26,43,60,13,30,47]	
		array = [[" " for i in range(0,4)] for j in range(0,64)]
		if r%4 == 1:
        		for i in range(0,64):
                                for j in range(0,4):
                                        array[i][j] = variable[index1[i]][j]
                elif r%4 == 3:
                        for i in range(0,64):
                                for j in range(0,4):
                                        array[i][j] = variable[index3[i]][j]
                else:
        		for i in range(0,64):
                                for j in range(0,4):
                                        array[i][j] = variable[i][j]                        
		return array	

	def Constrain(self,word,bit):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert(self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		#fileobj.write("Minimize\n")
		#fileobj.write("x_1_0_3\n")
		fileobj.write("Subject To\n")
		for i in range(0,64):
			for j in range(0,4):
				if ((word == i) & (bit ==j)):
					fileobj.write("x" + "_" + str(self.Round) + "_" +str(i) + "_" + str(j) + " = 1\n")
				else:
					fileobj.write("x" + "_" + str(self.Round) + "_" +str(i) + "_" + str(j) + " = 0\n")
		fileobj.close()
                for i in range(0,self.Round):
                        variablein = Saturnin.CreateVariables(i,"x")
                        variableout = Saturnin.CreateVariables(i,"y")
                        self.ConstraintsBySbox(variablein, variableout)
                        variablein = Saturnin.nibblePermut(variableout,i)
                        variableout= Saturnin.CreateVariables(i+1,"x")
                        variableout = Saturnin.nibblePermut(variableout,i)
                        self.ConstraintsByMDS(variablein,variableout,i)
	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0,self.Round):
                        for j in range(0,16):
                                for k in range(0,6):
                                        fileobj.write("t_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
			for j in range(0,64):
				for k in range(0,4):
					fileobj.write("x_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					fileobj.write("y_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					#fileobj.write("z_" + str(i) + "_" + str(j) + "_" + str(k))
					#fileobj.write("\n")
					fileobj.write("b_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					fileobj.write("e_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					fileobj.write("i_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
			for j in range(0,32):
				for k in range(0,4):
					fileobj.write("a_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					fileobj.write("c_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					fileobj.write("d_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					fileobj.write("f_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					fileobj.write("g_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					fileobj.write("h_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
					fileobj.write("j_" + str(i) + "_" + str(j) + "_" + str(k))
					fileobj.write("\n")
		fileobj.write("END")
		fileobj.close()

	def Init(self,counterInput):
		"""
		Generate the constraints introduced by the initial division property.
		"""
		variableout = Saturnin.CreateVariables(0,"x")
		fileobj = open(self.filename_model, "a")
		eqn = []
		for i in range(0,counterInput):
			temp = variableout[63 - (i / 4)][i%4] + " = 0"
			fileobj.write(temp)
			fileobj.write("\n")
		for i in range(counterInput, (counterInput+(self.activebits))%256):
			temp = variableout[63 - (i / 4)][i%4] + " = 1"
			fileobj.write(temp)
			fileobj.write("\n")
		for i in range((counterInput+(self.activebits))%256, 256):
			temp = variableout[63 - (i / 4)][i%4] + " = 0"
			fileobj.write(temp)
			fileobj.write("\n")
		fileobj.close()

	def MakeModel(self,counterInput,word,bit):
		"""
		Generate the MILP model of Saturnin given the round number and activebits.
		"""
		#self.CreateObjectiveFunction()
		self.Constrain(word,bit)
		self.Init(counterInput)
		self.VariableBinary()

	def WriteObjective(self, obj):
		"""
		Write the objective value into filename_result.
		"""
		fileobj = open(self.filename_result, "a")
		fileobj.write("The objective value = %d\n" %obj.getValue())
		eqn1 = []
		eqn2 = []
		for i in range(0, self.blocksize):
			u = obj.getVar(i)
			if u.getAttr("x") != 0:
				eqn1.append(u.getAttr('VarName'))
				eqn2.append(u.getAttr('x'))
		length = len(eqn1)
		for i in range(0,length):
			s = eqn1[i] + "=" + str(eqn2[i])
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()

	def SolveModel(self):
		"""
		Solve the MILP model to search the integral distinguisher of Saturnin.
		"""
		time_start = time.time()
		
		counter = 0
		counterInput = 0
		set_zero = []
		while counterInput < self.blocksize:
			counterInput += 1

			while counter < self.blocksize:
				self.filename_model = "Saturnin_" + str(self.Round) + "_" + str(self.activebits) + "_" + str(counterInput) + "_" + str(counter) + ".lp"
				self.MakeModel(counterInput-1,(counter/4),(counter%4))
				m = read(self.filename_model)
				m.params.threads=8
				#m.params.MIPFocus=1
				m.params.TimeLimit=7200
				time_start = time.time()
				m.optimize()
				counter += 1
				fileobj = open(self.filename_result, "a")
				fileobj.write("COUNTERINPUT = %d" % counterInput)
				fileobj.write("####COUNTER = %d" % counter)
				fileobj.close()
				# Gurobi syntax: m.Status == 2 represents the model is feasible.
				if m.Status == 2:
					fileobj = open(self.filename_result, "a")
					fileobj.write("*********COUNTERINPUT = %d" % counterInput)
					fileobj.write("*********COUNTER = %d feasible" % counter)
					fileobj.close()
					os.remove(self.filename_model)
				# Gurobi syntax: m.Status == 3 represents the model is infeasible.
				elif m.Status == 3:
					fileobj = open(self.filename_result, "a")
					fileobj.write("*********COUNTERINPUT = %d" % counterInput)
					fileobj.write("*********COUNTER = %d infeasible" % counter)
					fileobj.close()
					os.remove(self.filename_model)
				else:
					print "Unknown error!"
				
				time_end = time.time()
				fileobj = open(self.filename_result, "a")		
				fileobj.write(("**Time used = " + str(time_end - time_start) + "\n"))
				fileobj.close()
			counter = 0
		fileobj = open(self.filename_result, "a")		
		fileobj.write("\n")
		time_end = time.time()
		fileobj.write(("Time used = " + str(time_end - time_start)))
		fileobj.close()

