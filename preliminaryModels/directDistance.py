def dijkstra(graph):
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
    print(distances)
            



if __name__ == "__main__":
    graph = [[0, 2, 3, 2, 3, 5, 6], 
             [2, 0, 1, 4, 4, 5, 7],
             [3, 1, 0, 3, 4, 5, 9],
             [2, 4, 3, 0, 2, 4, 15],
             [3, 4, 4, 2, 0, 1, 9],
             [5, 5, 5, 4, 1, 0, 10],
             [6, 7, 9, 15, 9, 10, 0]]
    dijkstra(graph)
