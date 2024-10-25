# MINIMUM DISTANCE MODEL
import sys

# Determines the regret at each bus stop. Multiplies it by the bus stop capacity at the respective stop, and sums that to get the total system regret.
# Calculates regret at each stop by comparing the direct distances calculated in zeroRegretWithCapacities with the Minimum Distance Model here
# Can uncomment the print statements if running a model from the command line to see the stats
def calculate_regret(busRoutes, direct, pathSums, graph, capacities):
    for bus in busRoutes:
        stop = 2 # busRoute[0] = 0 and busRoute[1] is the first so the pathSums[busRoute[1]] is the path_distance so far, so only need to add the rest on top of that
        while stop < len(bus):
            pathSums[bus[stop]] += pathSums[bus[stop-1]]
            stop += 1
    regretAtBusStops = [pathSums[i+1] - direct[i] for i in range(len(direct))] # regret for each individual bus stop
    regret = [regretAtBusStops[i]*capacities[i+1] for i in range(len(regretAtBusStops))]

    # Uncomment these print statements to see more
    #print(pathSums[1:], " = path from source to each node i")
    #print(regretAtBusStops, " = regret experienced at each bus stop on the choice of routes in minimal distance model")
    #print(capacities[1:], " = capacities") # capacity of school is 0 since not transporting there
    #print(regret, " = regret at each bus stop multiplied by the number of students at each stop")
    #print(sum(regret), " = total regret of the system")
    # numStopsRegret = sum(x != 0 for x in regretAtBusStops)
    # print(f"The number of stops that experience regret is {numStopsRegret}")

    return sum(regret)


def calculate_total_distance(busRoutes, graph):
    total_distance = 0
    for bus in busRoutes:
        prev = bus[0]
        for stop in bus[1:]:
            total_distance += graph[prev][stop]
            prev = stop

    #print(total_distance, " = total distance travelled by all buses in this model")
    return total_distance


# This function finds which bus routes to take in when prioritising cost minimisation
# This is the Minimum Distance Model (MDM)
def greedyMinDistanceWithCapacities(graph, busLoad, capacities, directDistances):
    # set up
    source = 0
    n = len(graph) # number of bus stops
    G = [i for i in range(1, n)] # list of unvisited nodes, initially will be all nodes except the source
    current = [source]*n # keeps track of where the buses are -> the endpoints of the routes, initially all at the school
    busRoutes = [[source] for i in range(n)]
    busDistances = [0]*n
    loads = [busLoad]*n # before routing anywhere, all buses can take on busLoad number of students
    pathSums = [0]*n

    while len(G) > 0: # while there are still unvisited nodes
        min_dist = float('inf')
        minV = None
        path = None
        # grab the nearest unvisited node in the neighbourhood of edges outgoing from current bus positions in the graph
        for node in set(current):
            for v in G:
                if node != v and graph[node][v] < min_dist and loads[current.index(node)]-capacities[v] >= 0:
                    min_dist = graph[node][v]
                    minV = v # where we are going
                    path = node # where we currently are
        
        # ie. find the index of the relevant bus route, and update the current bus location (endpoint) to minV
        # update routes, distances and loads and remove node minV from G as it has now been visited
        busNumber = current.index(path)
        loads[busNumber] -= capacities[minV] # update how many people the bus can still transport after visiting this node
        current[busNumber] = minV
        busRoutes[busNumber].append(minV)
        busDistances[busNumber] += min_dist
        pathSums[minV] += min_dist
        G.remove(minV)
        
    # remove any redundant bus routes    
    busRoutes = [x for x in busRoutes if x != [0]]
    busDistances = [x for x in busDistances if x != 0]
    
    # If running capacitatedMinDistance.py from command line, can uncomment these print statements to see individual model stats
    # print(capacities, " = number of students being dropped off at each bus stop")
    # print(directDistances, " = direct distances from source to each node")
    # print(busRoutes, " = bus routes")
    # passengers = [busLoad - loads[i] for i in range(n) if busLoad - loads[i] != 0]
    # print(passengers, " = number of students travelling on each bus")
    # print(busDistances, " = distance each bus travels on its route")
    # print()
   
    totalRegret = calculate_regret(busRoutes, directDistances, pathSums, graph, capacities)
    totalDistance = calculate_total_distance(busRoutes, graph)
    
    return len(busRoutes), totalRegret, totalDistance

# To run the MDM from command line, you can pass in the busLoad, capacities file and adjacency matrix file to run a specific instance.
# capacities must be of the same form as anything in <n>stopsCapacities.txt
# If no parameters are passed in, the mock suburb will be run. Print statements may need to be uncommented to see the stats of the model
if __name__ == "__main__":
    # Expecting (optional) busLoad, (optional) capacities.txt, (optional) randomAdjMatrix.txt in arguments
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
                capacities = [0,*line]
        with open('directDistances.txt', 'r') as file:
            for line in file:
                line = line[1:-1].split(",")
                line = [int(i.strip()) for i in line]
                directDistances = line
    else:
        print("Expecting no arguments or the following 3: busLoad, capacities.txt, randomAdjMatrix.txt")
        sys.exit()
     
    
    graph = []
    with open(suburbFile, 'r') as file:
        for line in file:
            line = line[1:-2].split(",")
            line = [int(i.strip()) for i in line]
            graph.append(line)

    greedyMinDistanceWithCapacities(graph, busLoad, capacities, directDistances)