#!/usr/bin/env python

#This module implements the AHP algorithm.

__author__ = 'apprentice1989@gmail.com (Huang Shitao)'


import numpy as np


def calculate_weight(pairwises=[]):
	'''Define vector of weight based on eigenvector and eigenvalues'''
	eigenvalues, eigenvector = np.linalg.eig(pairwises)
	maxindex = np.argmax(eigenvalues)
	eigenvalues = np.float32(eigenvalues)
	eigenvector = np.float32(eigenvector)
	#extract vector from eigenvector with max vaue in eigenvalues
	weights = eigenvector[:, maxindex]
	#convert array(numpy)  to vector
	weights.tolist()
	weights = [w / sum(weights) for w in weights]
	return weights, eigenvalues, eigenvector


def consistency(weights, eigenvalues):
    '''Calculete Consistency index in accord with Saaty (1977)'''
    #order of matrix: 0,1,2,3,4,5,6,7,8
    RI = [0.00, 0.00, 0.00, 0.52, 0.90, 1.12, 1.24, 1.32, 1.41]
    order = len(weights)
    CI = (np.max(eigenvalues) - order) / (order - 1)
    return CI / RI[order - 1]


def test():
	'''example'''
	#pairwise = [[1.0,1/2.0,4.0,3.0,3.0],[2.0,1.0,7.0,5.0,5.0],[1/4.0,1/7.0,1.0,1/2.0,1.0/3.0],\
	#	[1/3.0,1/5.0,2.0,1.0,1.0],[1/3.0,1/5.0,3.0,1.0,1.0]]
	pairwises = [[1, 4.0], [1 / 4.0, 1]]
	weights, eigenvalues, eigenvector = calculate_weight(pairwises)
	consistency = consistency(weights, eigenvalues)
	print(weights)
	print(consistency)


if __name__ == '__main__':
	test()
