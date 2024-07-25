# multiply the regret at each bus stop by the capacity of that bus stop to get the total regret in the system
def calculate_direct_distances(graph):
    # find min path from source to all other nodes
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
        visited[minV] = True

        for v in range(len(graph)):
            if graph[minV][v] != 0 and not visited[v]: # checking alternate paths
                alt = distances[minV] + graph[minV][v]
                if alt < distances[v]:
                    distances[v] = alt
    return distances
    


def calculate_regret(visited, direct, path_distances, graph):
    distances = [i for i in path_distances]
    for busRoute in visited:
        stop = 2
        while stop < len(busRoute):
            distances[busRoute[stop]] += distances[busRoute[stop-1]]
            stop += 1
    print(distances) # correct

    regret = [distances[i] - direct[i] for i in range(len(direct))]
    print(regret) # not done right because of direct distances
    print(sum(regret))


def generalisedBuses(graph, source, busLoad, capacities):
     # set up
    G = []
    current = []
    visited = []
    loads = [busLoad]*len(graph) # set up loads to be the max
    directDistances = calculate_direct_distances(graph)
    pathDistances = [0]*len(graph)
    for v in range(len(graph)):
        G.append(v)
        current.append(source)
        visited.append([source])

    G.remove(source)

    while len(G) > 0:
        min_dist = float('inf')
        minV = None
        path = None
        # calculate all neighbours of all current vertices
        for node in set(current):
            print(set(current))
            # grab nearest from all of the current neighbours
            for v in G:
                if node != v and graph[node][v] < min_dist and loads[current.index(node)]-capacities[v] >= 0:
                    min_dist = graph[node][v]
                    minV = v
                    path = node
        # find index in current where element = node, and update that index
        
        print(loads)
        index = current.index(path) # is the bus number
        loads[index] -= capacities[minV]
        print(current.index(path), node)
        current[index] = minV
        visited[index].append(minV)
        pathDistances[minV] += min_dist
        G.remove(minV)
        print(min_dist, minV, path, current, directDistances, pathDistances)
        
    visited = [x for x in visited if x != [0]]
    print(visited, len(visited), directDistances)

    calculate_regret(visited, directDistances, pathDistances, graph)
    


if __name__ == "__main__":
    graph = [[0, 2, 3, 2, 3, 5, 6], 
             [2, 0, 1, 4, 4, 5, 7],
             [3, 1, 0, 3, 4, 5, 9],
             [2, 4, 3, 0, 2, 4, 15],
             [3, 4, 4, 2, 0, 1, 9],
             [5, 5, 5, 4, 1, 0, 10],
             [6, 7, 9, 15, 9, 10, 0]]
    capacities = [0,5, 1, 3, 3, 2, 4]
    busLoad = 5
    generalisedBuses(graph, 0, busLoad, capacities)