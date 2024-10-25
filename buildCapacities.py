import random
import sys

# This function randomises the number of students at each bus stop
# ie. the bus stop capacities c_i for i = {1,...,n} where n = # bus stops
# The bus load is set to 64 for this investigation
# To generate the desires bus stop capacities, input a different n in the arguments

if len(sys.argv) != 2:
    print("Please input number of bus stops as a parameter 8, 16, 32, 64 or 128.")
    sys.exit(1)
n = int(sys.argv[1])


smallest = float('inf')
largest = 0
with open(f'capacities/{n}stopsCapacities.txt', "w") as f:
    for j in range(100):
        arr = [1]*n # vary for number of bus stops n = 8, 16, 32, 64, 128
        for i in range(200-n): # vary this from 200 - n
            index = random.randint(0,n-1) # 0 to (n-1)
            while arr[index] >= 32: # stops bus stop capacity c_i exceeding half bus load 64
                index = random.randint(0,n-1) # 0 to (n-1)
            arr[index] += 1
        f.write(str(arr)+"\n")
        if min(arr) < smallest:
            smallest = min(arr)
        if max(arr) > largest:
            largest = max(arr)
    print(f'The smallest c_i is {smallest} and the largest is {largest}')
