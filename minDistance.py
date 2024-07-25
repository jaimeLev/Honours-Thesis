# function finds the distances from the source to each node in the network
# These direct distances form the baseline to compare the minimal distance model
# to gather the total regret and the regret for each individual
def calculate_direct_distances(graph):
    # find min path from source to all other nodes as a baseline to compare for regret
    distances = [float('inf')]*len(graph)
    distances[0] = 0
    visited = [False]*len(graph)

    for _ in range(len(graph)):
        min_dist = float('inf')
        minV = None
        for i in range(len(graph)):
            if not visited[i] and distances[i] < min_dist:
                min_dist = distances[i]
                minV = i
        
        if minV is None:
            break
        visited[minV] = True # don't cause loops

        for v in range(len(graph)):
            if graph[minV][v] != 0 and not visited[v]: # checking alternate paths
                alt = distances[minV] + graph[minV][v]
                if alt < distances[v]: # relaxation
                    distances[v] = alt
    return distances
    

# determines the regret for the students that they would experience at each bus stop
# compares the direct distances calculated with the minimal distance model
def calculate_regret(busRoutes, direct, path_distances, graph):
    print(busRoutes, " = bus routes")
    print(direct, " = direct distances from source to each node")
    for bus in busRoutes:
        stop = 2 # busRoute[0] = 0 and busRoute[1] is the first so the path_distances[busRoute[1]] is the path_distance so far so only need to add the rest on top of that
        while stop < len(bus):
            path_distances[bus[stop]] += path_distances[bus[stop-1]]
            stop += 1
    print(path_distances, " = path from source to each node i") # correct

    regret = [path_distances[i] - direct[i] for i in range(len(direct))] # regret for each individual bus stop
    print(regret, " = regret experienced at each bus stop on the choice of routes in minimal distance model")
    print(sum(regret), " = total regret of the system")


# the model to calculate which buses take which routes in a minimal distance model
def minDistance(graph, source):
    # set up
    G = [] # a list of unvisited nodes, intially will be all nodes excpet the source (where all buses start)
    current = [source]*len(graph) # a list of the nodes that the different buses are currently at
    busRoutes = [] #
    directDistances = calculate_direct_distances(graph)
    pathDistances = [0]*len(graph)
    for v in range(len(graph)):
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
                if node != v and graph[node][v] < min_dist:
                    min_dist = graph[node][v]
                    minV = v # where we are going
                    path = node
        # find index in current where element = node, and update that index
        # ie. find the index of the relevant bus route, and update the endpoint to minV
        # update route and distance and remove node minV as it has now been visited
        busNumber = current.index(path)
        current[busNumber] = minV
        busRoutes[busNumber].append(minV)
        pathDistances[minV] += min_dist
        G.remove(minV)
    
    # remove any redundant bus routes
    busRoutes = [x for x in busRoutes if x != [0]]

    calculate_regret(busRoutes, directDistances, pathDistances, graph)


if __name__ == "__main__":
    graph = [[0, 2, 3, 2, 3, 5, 6], 
             [2, 0, 1, 4, 4, 5, 7],
             [3, 1, 0, 3, 4, 5, 9],
             [2, 4, 3, 0, 2, 4, 15],
             [3, 4, 4, 2, 0, 1, 9],
             [5, 5, 5, 4, 1, 0, 10],
             [6, 7, 9, 15, 9, 10, 0]]
    minDistance(graph, 0)