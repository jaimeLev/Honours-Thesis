# ZERO REGRET MODEL
import sys

# TASK: Find min path from 0 to all other nodes. Only take a path is the bus can offload that amount of people
# STEP 1: Start with all buses taking immediate routes (using all n buses for n bus stops)
# STEP 2: Find the minimum edge weight (MEW) not yet evaluated.
# STEP 3: For all locations of this MEW, see if there's a path quicker than current, 
# and if we can drop off the additional students on that bus route. If so, relax!
# STEP 3: Repeat for the next highest MEW, until the MEW is >= the supremum path sum of any bus route.
def zeroRegret(graph, busLoad, capacities):
    # Set up: assume initially use all buses from source to all bus stop
    busRoutes = [] # nodes where buses travel on each route
    pathSums = [] # total distance of each route
    distances = [] # distance from source to every node in the model
    loads = [busLoad]*(len(graph)-1)
    current = [] # Holds the current bus positions
    for v in range(1, len(graph)):
        busRoutes.append([0, v]) # Step 1: create all paths from source to each stop
        pathSums.append(graph[0][v])
        distances.append(graph[0][v])
        loads[v-1] -= capacities[v]
        current.append(v)
    
    # find min edge distance, see if there's a relaxation with any edge with this weight that works with loads (bus stop capacity constraint)
    # exclusions is a list of all previous minimum edge weights (MEW) so we can iterate getting the next lowest greater than the current MEW
    exclusions = [0]
    matrixMin = 0
    while matrixMin != float('inf'):
        matrixMin = float('inf')
        for i in range(len(graph)):
            row = [j for j in graph[i] if j not in exclusions]
            if row == []:
                # If all edges outgoing from a node are in the exclusions list, we terminate early
                return distances, len(busRoutes)
            rowMin = min(row)
            if rowMin < matrixMin:
                matrixMin = rowMin
                locations = [(i, graph[i].index(matrixMin))]
            elif rowMin == matrixMin:
                if (graph[i].index(matrixMin), i) not in locations:
                    locations.append((i, graph[i].index(matrixMin)))
        
        exclusions.append(matrixMin)
        
        # locations is all edges that have the current min weight
        for location in locations:
            # need both endpoints of the min edge weight to be current bus positions of different routes
            if location[0] in current and location[1] in current:
                # find the indices (bus numbers) of which routes are at that current nodes on either side of the location edge
                for i in range(len(busRoutes)):
                    if location[0] in busRoutes[i]:
                        index0 = i
                    if location[1] in busRoutes[i]:
                        index1 = i
                
                altto1 = pathSums[index0] + matrixMin
                altto0 = pathSums[index1] + matrixMin
                
                # see if it relaxes the distance for one of the two routes
                if altto0 <= pathSums[index0]:
                    # see if it satisfies the bus stop capacity constraint -> we have enough spots to route the additional students on this route
                    if loads[index1] - capacities[location[0]] >= 0:
                        # update endpoint so location[0] is endpoint of route at index1
                        busRoutes[index1].append(location[0])

                        # delete location[0] from route at index0
                        busRoutes[index0].remove(location[0])

                        # update loads
                        loads[index1] -= capacities[location[0]]
                        loads[index0] += capacities[location[0]]

                        # update pathSums
                        pathSums[index1] = altto0
                        pathSums[index0] -= graph[location[0]][location[1]]

                        distances[location[0]-1] = altto0 # indexed from 1 so must remove 1
                        
                        # delete bus if necessary and associated metrics to that bus
                        if busRoutes[index0] == [0]:
                            busRoutes.pop(index0)
                            loads.pop(index0)
                            pathSums.pop(index0)
                        
                        current.remove(location[1])
                        
                elif altto1 <= pathSums[index1]:
                    # see if it satisfies the capacity constraints
                    if loads[index0] - capacities[location[1]] >= 0:
        
                        # update endpoint so location[1] is endpoint of route at index0
                        busRoutes[index0].append(location[1])

                        # delete location[1] from route at index1 and delete bus if relevant
                        busRoutes[index1].remove(location[1])

                        # update loads
                        loads[index0] -= capacities[location[1]]
                        loads[index1] += capacities[location[1]]

                        # update pathSums
                        pathSums[index0] = altto1
                        pathSums[index1] -= graph[location[0]][location[1]]
                        distances[location[1]-1] = altto1
                        
                        # delete bus if necessary and associated metrics
                        if busRoutes[index1] == [0]:
                            busRoutes.pop(index1)
                            loads.pop(index1)
                            pathSums.pop(index1)

                        current.remove(location[0])

    # Uncomment these print statements to see more                
    #print(capacities, " = how many students at each bus stop")
    #print(distances, " = distances found from source to every node")
    #print(busRoutes, " = bus routes")
    #passengers = [busLoad - loads[i] for i in range(len(loads)) if busLoad - loads[i] != 0]
    #print(passengers, " = number of students travelling on each bus")
    #print(pathSums, " = the distance that each bus travels on its route")
    #print(sum(pathSums), " = the total distance travelled by all buses in this model")

    return distances, len(busRoutes)
                    

# To run the MDM from command line, you can pass in the busLoad, capacities file and adjacency matrix file to run a specific instance.
# capacities must be of the same form as anything in <n>stopsCapacities.txt
# If no parameters are passed in, the mock suburb will be run. Print statements may need to be uncommented to see the stats of the model
if __name__ == "__main__":
    # Expecting (optional) busLoad, capacities.txt, randomAdjacencyMatrix.txt.
    capacities = []
    directDistances = []
    busLoad = 10
    if len(sys.argv) == 1:
        suburbFile = 'mockSuburb.txt'
        capacities = [0, 5, 6, 3, 3, 2, 4]
        directDistances = [2,3,2,3,4,6]
    elif len(sys.argv) == 4:
        suburbFile = sys.argv[3]
        busLoad = int(sys.argv[1]) 
        with open('capacities.txt', 'r') as file:
            for line in file:
                line = line[1:-1].split(",")
                line = [int(i.strip()) for i in line]
                capacities = line
    else:
        print("Expecting no arguments or the following 3: busLoad, capacities.txt, randomAdjMatrix.txt")
        sys.exit()

    graph = []
    with open(suburbFile, 'r') as file:
        for line in file:
            line = line[1:-2].split(",")
            line = [int(i.strip()) for i in line]
            graph.append(line)

    directDistances, numBuses = zeroRegret(graph, busLoad, capacities)
    with open('busLoad.txt', 'w') as file:
        file.write(str(busLoad))
    
    with open('directDistances.txt', 'w') as file:
        file.write(str(directDistances))
