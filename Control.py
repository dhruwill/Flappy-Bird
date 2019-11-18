import numpy as np
import math
import Genetic
import NeuralNets as NN

CR = .9 # Crossover Rate
MR = .05 # Mutation Rate
generations = 50 # Number of Generations
netsize = 20 # Number of Neural Networks in a Generation

genome=[] # List of Neural Networks in current Generation
for i in range (0,netsize):
    netelement = NN.NeuralNet() # Creating a neural network to be a part of the current generation
    genome.append(netelement) # Adding the current neural network to the group containing the rest of the current generation

for i in range(0,generations):
    print 'GENERATION ' + str(i) # Printing the generation under progress
    genome = newnetlist(genome) # Evolution from current generation to next generation
    genome = sorted(genome, key=performance,reverse=True) # Arranging all the neural networks of current generation on the basis of decreasing order of performance
    play(False, genome[0]) # Playing the game on the basis of the best performing neural network of the current generation
