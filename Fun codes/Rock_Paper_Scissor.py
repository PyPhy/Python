#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint

player = input('rock (r), paper (p) or scissors (s)? : ')

comp = randint(1,3)

if comp == 1:
    computer = 'r'
    print('r vs ' + player)
    
    if player == 'r':
        print('Draw !!!')
    elif player == 'p':
        print('player wins !!!')
    elif player == 's':
        print('computer wins !!!')
    
elif comp == 2:
    computer = 'p'
    print('p vs ' + player)
    
    if player == 'r':
        print('computer wins !!!')
    elif player == 'p':
        print('Draw !!!')
    elif player == 's':
        print('player wins !!!')
    
elif comp == 3:
    computer = 's'
    print('s vs ' + player)
    
    if player == 'r':
        print('player wins !!!')
    elif player == 'p':
        print('computer wins !!!')
    elif player == 's':
        print('Draw !!!')
