def printPaths(graph, prevs):
    #printing the paths
    paths = []
    for i in range(1, len(graph)):
        j = i
        path = [0]
        while prevs[j] != 0:
            print(i, j, prevs[j])
            path.append(prevs[j])
            j = prevs[j]
        path.append(i)
        paths.append(path)


    # removing the subsets
    toRemove = []
    for i in range(len(paths)):
        for j in range(i+1, len(paths)):
            if set(paths[i]).issubset(paths[j]):
                toRemove.append(i)

    paths = [paths[i] for i in range(len(paths)) if i not in toRemove]
    
    print(paths)


def zeroRegret(graph, busLoad, capacities):
    # find min path from source to all other nodes
    G = []
    for v in range(len(graph)):
        G.append(v)
    routes = [[0]]*len(graph)
    distances = [float('inf')]*len(graph) # distances of the paths
    distances[0] = 0
    visited = [False]*len(graph)
    loads = [busLoad]*len(graph)
    current = [0]*len(graph)
    prevs = [0]*len(graph) # routes of the paths
    #prevs[0] = None
    print(prevs)
    G.remove(0)
    busIndex = 0


    for node in range(len(graph)):
        min_dist = float('inf')
        minV = None
        print(distances)
        for i in range(len(graph)): # find next shortest
            if node != i and not visited[i] and graph[node][i] < min_dist and loads[node]-capacities[i] >= 0:
                print(distances[i], i)
                min_dist = graph[node][i]
                minV = i
        
        if minV is None:
            break
        
        #loads not on node but on bus track have to do prevs
        if node == 0 or minV == 0:
            # new bus
            print(minV, node)
            if minV != 0:
                routes[busIndex].append(minV)
                loads[busIndex] -= capacities[minV]
                current[busIndex] = minV
            else:
                routes[busIndex].append(node)
                loads[busIndex] -= capacities[node]
                current[busIndex] = node
            busIndex += 1
        else:
            # find the prev and attach it to their load
            print(minV, node, prevs, " not 0", visited, current)
            if node in current:
                print("node in current")
                index = current.index(node)
                if loads[index] - capacities[minV] >= 0:
                    # choose this index otherwise skip
                    loads[index] -= capacities[minV] # of the bus its on the route for
                # need to bring this up before i select it as min_dist, if it doesn't satisfy capacity constraints need to move onto next smallest
        print("new edge is ", minV, node, graph[minV][node], loads, routes)
        visited[minV] = True

        for v in range(len(graph)): # relaxation
            if graph[minV][v] != 0 and not visited[v]: # checking alternate paths
                alt = distances[minV] + graph[minV][v]
                if alt <= distances[v]:
                    prevs[v] = minV
                    distances[v] = alt
            
 
    
    print(distances)
    print(prevs)
    print(routes)

    # for i in range(1, len(graph)):
    #     printPaths(prevs, i)

    printPaths(graph, prevs)



if __name__ == "__main__":
    graph = [[0, 2, 3, 2, 3, 5, 6], 
             [2, 0, 1, 4, 4, 5, 7],
             [3, 1, 0, 3, 4, 5, 9],
             [2, 4, 3, 0, 2, 4, 15],
             [3, 4, 4, 2, 0, 1, 9],
             [5, 5, 5, 4, 1, 0, 10],
             [6, 7, 9, 15, 9, 10, 0]]
    capacities = [0, 5, 1, 3, 3, 2, 4]
    busLoad = 5
    zeroRegret(graph, busLoad, capacities)
