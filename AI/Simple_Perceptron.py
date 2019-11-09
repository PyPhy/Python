#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import random, exp, dot, array

#%% Neural Network

class Neural_Network():
    
    #%% Sigmoid function
    def φ(self, x):
        
        return 1/(1 + exp(-x))

    # Sigmoid function's derivative
    def dφ(self, x):
        
        return exp(x)/ (1 + exp(x))**2
    
    #%% Let's train our Neuron
    
    def __init__(self, x, y, lr, epochs):
        
        '''
            x:      training input (dimentions: parameters* data)
            y:      training output (dimentions: parameters* data)
            lr:     learning rate
            epochs: iterations
        '''
        
        # same random number
        random.seed(1)
        
        # weights (dimentions: perceptrons* parameters)
        self.w = 2* random.random( (1,3) ) - 1
        
        print('Initial weights: ', self.w)
        
        for epoch in range(epochs):
            
            # learning output
            Y = self.φ( dot(self.w, x) )
            
            # error = training output - learning output
            error = y - Y
            
            # adjustments to minimize the error
            adjustments = error* self.dφ(Y)
            
            # adjusted weights
            self.w += lr* dot(adjustments, x.T)
            
        print('Trained weights: ', self.w)
    
    #%% I shall give a problem
    
    def think(self, inputs):
        
        return self.φ( dot(self.w, inputs) )
    
#%% Main file

if __name__ == '__main__':

    #%% Train the neuron first
    
    # 3 rows means 3 input types i.e. 3 xi
    training_inputs = array([[0, 1, 1, 0],
                             [0, 1, 0, 1],
                             [1, 1, 1, 1] ])
    
    # each output correspondces to input 1 row
    training_outputs = array([ [0, 1, 1, 0] ])
    
    # object created
    NN = Neural_Network(training_inputs, training_outputs, 0.1, 10000)
    
    #%% Now guess the output
    
    Guess_Input = array([ [0],
                          [0],
                          [1] ])
    
    print('Guessed output is...')
    print( NN.think(Guess_Input))
