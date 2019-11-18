from flappygame import play
import random
from random import randint
import numpy as np
import math
import NeuralNets as NN

CR = .9 # Crossover Rate
MR = .05 # Mutation Rate

def performance(n):
    return play(False,n) # Returning the score of the current neural network


def updateweights(n1, n2):
    a = random.random() # Random value to decide whether or not crossover occurs
    WL1 = np.array(n1.nettolist()) # Converting the W1 and W2 of the current neural network into a list and further converting it into an array
    WL2 = np.array(n2.nettolist()) # Converting the W1 and W2 of the current neural network into a list and further converting it into an array
    C1 = WL1
    C2 = WL2
    if a < CR: # Checking the condition for crossover
		C1 = [i * 0.5 for i in np.add(WL1, WL2)] # Assigning C1 the average of the above weights
		C2 = [i * 0.5 for i in np.add(WL1, WL2)] # Assigning C2 the average of the above weights

    b = random.random() # Random value to decide whether or not mutation occurs for the first neural network
    c = random.random() # Random value to decide whether or not mutation occurs for the second neural network
    if b < MR: # Checking condition for mutation for first neural network
	    index = random.randint(0, len(C1) - 1) # Choosing a random weight to be mutated
	    C1[index] += random.triangular(-1, 1) * C1[index] # Using triangular distribution to mutate the weight proportional to its current value
    if c < MR: # Checking condition for mutation for first neural network
        index = random.randint(0, len(C2) - 1) # Choosing a random weight to be mutated
        C2[index] += random.triangular(-1, 1) * C2[index] # Using triangular distribution to mutate the weight proportional to its current value

    n1.listtonet(C1) # Assigning the values of W1 and W2 of the current neural network on the basis of the array of weights obtained from above
    n2.listtonet(C2) # Assigning the values of W1 and W2 of the current neural network on the basis of the array of weights obtained from above
    return (n1, n2) # Returning the neural networks for the next generation

def survivaloffittest(genome):
    first = genome[random.randint(0, len(genome) - 1)] # Choosing a random neural network of the current generation
    second = genome[random.randint(0, len(genome) - 1)] # Choosing a random neural network of the current generation
    if performance(first) > performance(second): # Returning the better of the two neural networks on the basis of performance
        return first
    else:
        return second

def newnetlist(genome):
	newnetlist = [] # Creating a list to contain the neural networks of the next generation
	genome = sorted(genome, key=performance,reverse=True) # Arranging all the neural networks of current generation on the basis of decreasing order of performance
	newnetlist.extend(genome[0:6]) # Carrying the six highest scoring neural networks forward to the next generation

	while len(newnetlist) < len(genome): # Filling the remaining 14 positions in the next generation
		first = survivaloffittest(genome) # Selecting two random neural networks of the current generation and choosing the better amongst them
		second = survivaloffittest(genome) # Selecting two random neural networks of the current generation and choosing the better amongst them
		first, second = updateweights(first, second) # Using the neural networks of the current generation to create neural networks for the next generation
		newnetlist.append(first) # Adding the new neural network to the next generation
        newnetlist.append(second) # Adding the new neural network to the next generation
	return newnetlist # Returning the list containing the neural networks of the next generation
