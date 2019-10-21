#!/usr/bin/env python3

import time
import threading

def calc_square(numbers):
    print('calculate square numbers')
    for n in numbers:
        time.sleep(0.2)
        print('square:', n**2)

def calc_cube(numbers):
    print('calculate cube of numbers')
    for n in numbers:
        time.sleep(0.2)
        print('cube:', n**2)

arr = [2, 3, 8, 9]

t = time.time()

#%% This is the simple way. Without threading it take about 1.6 seconds
# calc_square(arr)
# calc_cube(arr)

#%% Now let's use thread

# here we are first targeting the function using "target"
# then we are giving arguments to that target function
t1 = threading.Thread(target=calc_square, args=(arr,))
t2 = threading.Thread(target=calc_cube, args=(arr,))

# so we have created two threads
# Let's start it now
t1.start()
t2.start()

# now wait till other process is done
t1.join()
t2.join()

print('done in:', time.time() - t)
print('Hah... I am done with all my work now!')
