import random
import math
import sys

# This function generates the randomised adjacency matrix.
# Given the number of bus of bus stops n, and the the suburb size l
# It will generate the random locations of the bus stops and return the adjacency matrix based off the Euclidean distance between nodes


def generateRandomMatrix(n, l):
    length = l/2
    locations = [(0,0)] # start with the school
    sign = [-1,1]
    # loop to generate n unique random locations in the suburb
    for i in range(n):
        location = (random.randint(0, length)*random.choice(sign), random.randint(0, length)*random.choice(sign))
        while location in locations:
            location = (random.randint(0, length)*random.choice(sign), random.randint(0, length)*random.choice(sign))
        locations.append(location)

    # forming the adjacency matrix by calculating the Euclidean distance between every pair of nodes
    adjacencyMatrix = []
    for node0 in locations:
        distanceRow = []
        for node1 in locations:
            if node0 == node1:
                distanceRow.append(0)
            else:
                # calculates the Euclidean distances from the node to the school
                distance = math.sqrt((node1[0] - node0[0])**2 + (node1[1] - node0[1])**2)
                distanceRow.append(int(round(distance, 0)))
        adjacencyMatrix.append(distanceRow)
    return adjacencyMatrix

# This function can also be run on the command line when you pass in n and l as arguments
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Please enter parameters n and l, for # bus stops and suburb size")
    else:
        n = int(sys.argv[1])
        l = int(sys.argv[2])
        
        adjacencyMatrix = generateRandomMatrix(n,l)
        with open('randomAdjMatrix.txt', 'w') as file:
            for line in adjacencyMatrix:
                file.write(str(line) + "\n")