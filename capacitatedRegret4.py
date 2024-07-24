# may be able to terminate earlier, potentially if one iteration doesn't change can stop

def zeroRegret(graph, busLoad, capacities):
    # find min path from 0 to all other nodes. Only take a path is the bus can offload that amount of people
    # start with all buses taking direct routes
    # set up initially distances of the paths
    # set up initial bus loads
    # set up endpoints
    paths = []
    busDistances = []
    distances = []
    loads = [busLoad]*(len(graph)-1)
    endpoints = []
    for v in range(1, len(graph)):
        paths.append([0, v])
        busDistances.append(graph[0][v])
        distances.append(graph[0][v])
        loads[v-1] -= capacities[v]
        endpoints.append(v)
    #print(paths, busDistances, loads)

   

    # find min edge distance
    exclusions = [0]
    exit = False
    matrixMin = 0
    while matrixMin != float('inf'):

        matrixMin = float('inf')
        for i in range(len(graph)):
            row = [j for j in graph[i] if j not in exclusions]
            if row == []:
                exit = True
                break
            rowMin = min(row)
            if rowMin < matrixMin:
                matrixMin = rowMin
                locations = [(i, graph[i].index(matrixMin))]
            elif rowMin == matrixMin:
                if (graph[i].index(matrixMin), i) not in locations:
                    locations.append((i, graph[i].index(matrixMin)))
        
        if exit:
            break
        exclusions.append(matrixMin)
        
        

        for location in locations:
            if location[0] in endpoints and location[1] in endpoints:
                # find the indices of which routes hold those endpoints
                for i in range(len(paths)):
                    if location[0] in paths[i]:
                        index0 = i
                    if location[1] in paths[i]:
                        index1 = i
                altto1 = busDistances[index0] + graph[location[0]][location[1]]
                altto0 = busDistances[index1] + graph[location[0]][location[1]]
                #print(altto1, busDistances[index1], altto0, busDistances[index0],loads[index1], loads[index0], loads[index1] - capacities[location[0]], loads[index0] - capacities[location[1]])

                # see if it relaxes the distance for one of the two routes
                if altto0 <= busDistances[index0]:
                    # see if it satisfies the capacity constraints
                    if loads[index1] - capacities[location[0]] >= 0:
                        # update endpoint so location[0] is endpoint of route at index1
                        paths[index1].append(location[0])

                        # delete location[0] from route at index0
                        paths[index0].remove(location[0])

                        # update loads
                        loads[index1] -= capacities[location[0]]
                        loads[index0] += capacities[location[0]]

                        # update busDistances
                        busDistances[index1] = altto0
                        busDistances[index0] -= graph[location[0]][location[1]]

                        #distances[index1] = altto0
                        distances[index0] -= graph[location[0]][location[1]]
                        
                        # delete bus if necessary and same indices if relevant
                        if paths[index0] == [0]:
                            paths.pop(index0)
                            loads.pop(index0)
                            busDistances.pop(index0)
                        
                        endpoints.remove(location[1])
                        
                        

                if altto1 <= busDistances[index1]:
                    # see if it satisfies the capacity constraints
                    if loads[index0] - capacities[location[1]] >= 0:
        
                        # update endpoint so location[1] is endpoint of route at index0
                        paths[index0].append(location[1])

                        # delete location[1] from route at index1 and delete bus if relevant
                        paths[index1].remove(location[1])

                        # update loads
                        loads[index0] -= capacities[location[1]]
                        loads[index1] += capacities[location[1]]

                        # update busDistances
                        busDistances[index0] = altto1
                        busDistances[index1] -= graph[location[0]][location[1]]

                        #distances[index0] = altto1
                        distances[index1] -= graph[location[0]][location[1]]
                        
                        # delete bus if necessary and same indices if relevant
                        if paths[index1] == [0]:
                            paths.pop(index1)
                            loads.pop(index1)
                            busDistances.pop(index1)

                        endpoints.remove(location[0])
                        
    print(paths, loads, busDistances, distances)
                    






    
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
