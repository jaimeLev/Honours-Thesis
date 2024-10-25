import random
import math
import capacitatedZeroRegret
import capacitatedMinDistance
from randomAdjacencyMatrix import generateRandomMatrix
import buildCapacities
import csv
import time
import sys

# To run this script, vary the file name <n>stopsCapacities.txt where n is the number of bus stops in the model you wish you create
# Vary n in the first line, for powers of 2, ie. n = 8,16,32,64...
# Rename the output csv files accordingly in the format <n>by<size> where size denotes the length of the suburb from the center (school) to one side.
#   i.e. size 16 means the suburb where we can put locations in is 32 x 32 -> This needs to be reflected in randomAdjacencyMatrix.py (it is relative to this n)
# Other parameters can be changed if desired eg. busLoad, the number of repetitions of capacities and random locations

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Enter parameters n = {8, 16, 32, 64, 128} for # of bus stops and l = {16, 32, 64, 128} for suburb size")
        sys.exit(1)
        
    n = int(sys.argv[1]) # change this between 8, 16, 32, 64 and 128 for number of bus stops
    l = int(sys.argv[2]) # change this between 16, 32, 64 and 128 for size of the suburb
    if n not in [8,16,32,64,128]:
        print("Not a valid n")
        sys.exit(1)
    if l not in [16,32,64,128]:
        print("Not a valid l")
        sys.exit(1)
    busLoad = 64 # FIXED for this investigation
    numStudents = 200 # FIXED for this investigation

    with open(f"results/n{n}byl{l}for{numStudents}StudentstransportingMax{busLoad}.csv", 'w') as fout:
        line = ["location index", "capacity index", "total regret", "extra distance", "extra buses"]
        o=csv.writer(fout)
        o.writerow(line)
        avgZRMTime = 0
        avgMDMTime = 0
        start = time.time()
        for k in range(100): 
            # make a random adjacency matrix and run on 100 different capacities
            graph = generateRandomMatrix(n, l)
            for j in range(100):
                capacities = buildCapacities.randomiseCapacities(n, busLoad, numStudents)
                
                ZRM_start = time.time()
                directDistances, numZRMBuses = capacitatedZeroRegret.zeroRegret(graph, busLoad, capacities)
                avgZRMTime += time.time() - ZRM_start
                
                MDM_start = time.time()
                numMDMBuses, totalRegret, MDMDistance = capacitatedMinDistance.greedyMinDistance(graph, busLoad, capacities, directDistances)
                avgZRMTime += time.time() - ZRM_start
                
                line = [k, j, totalRegret, sum(directDistances)-MDMDistance, numZRMBuses-numMDMBuses]
                o.writerow(line)
            
        time = time.time() - start
        avgZRMTime = float(avgZRMTime/10000)
        avgMDMTime = float(avgMDMTime/10000)
        o.writerow(["","", "Time to complete", "Avg time of ZRM iteration", "Avg time of MDM iteration"])
        o.writerow(["","", time, avgZRMTime, avgMDMTime])
