import random
import sys

# This function randomises the number of students at each bus stop
# ie. the bus stop capacities c_i for i = {1,...,n} where n = # bus stops
# The bus load is set to 64 for this investigation
# We also have 200 students in this investigation
# To generate the desires bus stop capacities, input a different n in the arguments

def randomiseCapacities(n, busLoad, numStudents):
    bins = [1]*n # vary for number of bus stops n = 8, 16, 32, 64, 128
    for i in range(numStudents-n):
        index = random.randint(0,n-1)
        while bins[index] >= busLoad/2: # stops bus stop capacity c_i exceeding half bus load 64
            index = random.randint(0,n-1)
        bins[index] += 1
    return [0, *bins]

# Input the number of bus stops n in the arguments to generate the random capacities
# Can also input the busLoad and numStudents as the code is customisable, but if empty will go with the default
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please input number of bus stops as a parameter 8, 16, 32, 64 or 128.")
        sys.exit(1)
    n = int(sys.argv[1])
    capacities = randomiseCapacities(n, busLoad=64, numStudents=200)
    with open('capacities.txt', "w") as f:
        f.write(str(capacities))
