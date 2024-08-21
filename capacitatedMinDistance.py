# multiply the regret at each bus stop by the capacity of that bus stop to get the total regret in the system

# function finds the distances from the source to each node in the network
# These direct distances form the baseline to compare the minimal distance model
# to gather the total regret and the regret for each individual
def calculate_direct_distances(graph, n):
    # find min path from source to all other nodes
    distances = [float('inf')]*n
    distances[0] = 0
    visited = [False]*n

    for _ in range(n):
        min_dist = float('inf')
        minV = None
        for i in range(n):
            if not visited[i] and distances[i] < min_dist:
                min_dist = distances[i]
                minV = i
        
        if minV is None:
            break
        visited[minV] = True # stops loops being formed

        for v in range(n):
            if graph[minV][v] != 0 and not visited[v]: # checking alternate paths
                alt = distances[minV] + graph[minV][v]
                if alt < distances[v]: # relaxation
                    distances[v] = alt
    return distances
    


# determines the regret for the students that they would experience at each bus stop
# compares the direct distances calculated with the minimal distance model
def calculate_regret(busRoutes, direct, path_distances, graph, capacities):
    for bus in busRoutes:
        stop = 2 # busRoute[0] = 0 and busRoute[1] is the first so the path_distances[busRoute[1]] is the path_distance so far so only need to add the rest on top of that
        while stop < len(bus):
            path_distances[bus[stop]] += path_distances[bus[stop-1]]
            stop += 1
    print(path_distances, " = path from source to each node i") # correct

    regretAtBusStops = [path_distances[i+1] - direct[i] for i in range(len(direct))] # regret for each individual bus stop
    print(regretAtBusStops, " = regret experienced at each bus stop on the choice of routes in minimal distance model")
    print(capacities, " = capacities")
    regret = [regretAtBusStops[i]*capacities[i+1] for i in range(len(regretAtBusStops))]
    print(regret, " = regret at each bus stop multiplied by the number of students at each stop")
    print(sum(regret), " = total regret of the system")


# the model to calculate which buses take which routes in a minimal distance model
def capacitatedMinDistance(graph, source, busLoad, capacities, directDistances):
    # set up
    n = len(graph)
    G = [] # list of unvisited nodes, initially will be all nodes except the source
    current = [source]*n
    busRoutes = []
    loads = [busLoad]*n # set up loads to be the max
    #directDistances = calculate_direct_distances(graph, n)
    pathDistances = [0]*n
    for v in range(n):
        G.append(v)
        busRoutes.append([source])

    G.remove(source)

    while len(G) > 0: # while there are still unvisited nodes
        min_dist = float('inf')
        minV = None
        path = None
        # grab the nearest unvisited neighbouring node from all of the current positions of the buses in the network
        for node in set(current):
            for v in G:
                if node != v and graph[node][v] < min_dist and loads[current.index(node)]-capacities[v] >= 0:
                    min_dist = graph[node][v]
                    minV = v # where we are going
                    path = node
        # find index in current where element = node, and update that index
        # ie. find the index of the relevant bus route, and update the endpoint to minV
        # update route and distance and remove node minV as it has now been visited
        
        busNumber = current.index(path)
        loads[busNumber] -= capacities[minV] # update how many people the bus can still transport after visiting this node
        current[busNumber] = minV
        busRoutes[busNumber].append(minV)
        pathDistances[minV] += min_dist
        G.remove(minV)
        
    # remove any redundant bus routes    
    busRoutes = [x for x in busRoutes if x != [0]]
    
    print(capacities, " = number of students being dropped off at each bus stop")
    print(directDistances, " = direct distances from source to each node")
    print(busRoutes, " = bus routes")
    passengers = [busLoad - loads[i] for i in range(n) if busLoad - loads[i] != 0]
    print(passengers, " = number of students travelling on each bus")
    print()
   
    calculate_regret(busRoutes, directDistances, pathDistances, graph, capacities)
    


if __name__ == "__main__":
    graph = [[0, 2, 3, 2, 3, 5, 6], 
             [2, 0, 1, 4, 4, 5, 7],
             [3, 1, 0, 3, 4, 5, 9],
             [2, 4, 3, 0, 2, 4, 15],
             [3, 4, 4, 2, 0, 1, 9],
             [5, 5, 5, 4, 1, 0, 10],
             [6, 7, 9, 15, 9, 10, 0]]
    # graph = []
    # with open('randomMatrix.txt', 'r') as file:
    #     for line in file:
    #         line = line[1:-2].split(",")
    #         line = [int(i.strip()) for i in line]
    #         graph.append(line)
    #capacities = [0,5, 1, 3, 3, 2, 4]
    busLoad = None
    with open('busLoad.txt', 'r') as file:
        for line in file:
            busLoad = int(line)
    capacities = []
    with open('capacities.txt', 'r') as file:
        for line in file:
            line = line[1:-1].split(",")
          
            line = [int(i.strip()) for i in line]
            capacities = line
    print(capacities)
    directDistances = []
    with open('directDistances.txt', 'r') as file:
        for line in file:
            line = line[1:-2].split(",")
            
            line = line[:-1]
            line = [int(i.strip()) for i in line]
            directDistances = line

    capacitatedMinDistance(graph, 0, busLoad, capacities, directDistances)