import numpy as np
import math
from flappygame import play
import random

base = [-0.252165132632152, -0.125465654654654165, -0.62625521521526,-0.365545284852,-0.4054554656265656,1.982126516512] #Trained Data after 50 Generations
#base = [0,0,0,0,0,0] #Initial Weights
class NeuralNet():

    def __init__(self, W1=None, W2=None): # Constructor to the Neural Network
        self.InpNodes = 2 # Number of Input Nodes
        self.HiddenNodes = 2 # Number of Hidden Nodes
        self.OutNodes = 1 # Number of Output Nodes
        if W1 and W2:
            self.W1 = W1 # Assigning the weigths to connections between input and hidden layers
            self.W2 = W2 # Assigning the weigths to connections between hidden and output layers
        else:
            self.random() # Initialising the weights using triangular initialisation

    def random(self):
        weightslist = [] # List of Weights to be passed on to the next generation
        for weight in base:
            weightslist.append(weight + random.triangular(weight - .3, weight + .3)) # Using the weight from current generation (Initial only) along with triangular initialisation to create corresponding weight for next generation
        self.listtonet(weightslist) # Establishing appropriate values for W1 and W2 in order to create next generation

    def listtonet(self, weightslist):
        W1 = [] # Creating a list for connections between input and hidden layers (Size 4) (List of lists)
        W2 = [] # Creating a list for connections between hidden and output layers (Size 2) (List of lists)
        count = 0 # Creating a counter variable
        for i in xrange(self.InpNodes):
            n = [] # Creating a temporary list of elements connected to the current input node
            for j in xrange(self.HiddenNodes):
                n.append(weightslist[count]) # Filling the necessary values in the list of nodes of the current element (Assume it to be an adjacency list where instead of storing the vertex connected we store the weight of the edge)
                count += 1 # Changing counter Variable
            W1.append(n) # Adding the list of size 2 to the list W1
        # W1 represents a list of lists consisting of two lists of size 2 each
        for i in xrange(self.HiddenNodes):
            n = [] # Creating a temporary list of elements connected to the current hidden node
            for j in xrange(self.OutNodes):
                n.append(weightslist[count]) # Filling the necessary values in the list of nodes of the current element (Assume it to be an adjacency list where instead of storing the vertex connected we store the weight of the edge)
                count += 1 # Changing counter Variable
            W2.append(n) # Adding the list of size 1 to the list W2
        # W2 represents a list of lists consisting of two lists of size 1 each
        self.W1 = W1 # Assigning the weigths to connections between input and hidden layers
        self.W2 = W2 # Assigning the weigths to connections between hidden and output layers

    def forward(self, inputvalues): # Input values is list of values of size 2 (1 x 2 matrix)
        hiddenlayeroutput = self.sigmoid(np.dot(inputvalues, self.W1)) # Hidden layer output is activation values of the nodes of the hidden layer derived from the dot product between the input list and the W1 from the current neural network and applying the sigmoid function on it
        output = self.sigmoid(np.dot(hiddenlayeroutput, self.W2)) # Output is activation value of the output node derived from the dot product between the hidden layer output and the W2 from the current neural network and applying the sigmoid function on it
        return output # Returning the activation value determined by the current neural network in order to decide whether or not to flap under the current circumstances

    def nettolist(self):
	weightslist = [] # Creating a list of weights from W1 and W2 since they are lists of lists
        for i in self.W1:
            weightslist.extend(i) # Breaking down each list in W1 to values and adding it to weightslist
	for i in self.W2:
            weightslist.extend(i) # Breaking down each list in W2 to values and adding it to weightslist
        return weightslist # Returning the weightlist in the form a single list of containing six double values


    def sigmoid(self, n):
        return 1/(1 + np.exp(-n))
