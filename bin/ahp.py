#!/usr/bin/env python

import numpy as np

def calculateWeight(pairwise = []):
	"Define vector of weight based on eigenvector and eigenvalues"
	eigenvalues, eigenvector = np.linalg.eig(pairwise)
	maxindex = np.argmax(eigenvalues)
	eigenvalues = np.float32(eigenvalues)
	eigenvector = np.float32(eigenvector)
	weight = eigenvector[:, maxindex] #extract vector from eigenvector with max vaue in eigenvalues
	weight.tolist() #convert array(numpy)  to vector
	weight = [ w/sum(weight) for w in weight ]
	return weight, eigenvalues,  eigenvector

def Consistency(weight, eigenvalues):
    "Calculete Consistency index in accord with Saaty (1977)"
    RI = [0.00, 0.00, 0.00,0.52,0.90,1.12,1.24,1.32,1.41]     #order of matrix: 0,1,2,3,4,5,6,7,8
    order = len(weight)
    CI = (np.max(eigenvalues)-order)/(order-1)
    return CI/RI[order-1]
    
def example():
	"example"
	#pairwise = [[1.0,1/2.0,4.0,3.0,3.0],[2.0,1.0,7.0,5.0,5.0],[1/4.0,1/7.0,1.0,1/2.0,1.0/3.0],\
	#	[1/3.0,1/5.0,2.0,1.0,1.0],[1/3.0,1/5.0,3.0,1.0,1.0]]
	pairwise = [[1,4.0],[1/4.0,1]]
	weight, eigenvalues, eigenvector = calculateWeight(pairwise)
	consistency = Consistency(weight,eigenvalues)
	print(weight)
	print(consistency)
