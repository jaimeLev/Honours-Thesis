def dijkstra(graph, source):
    # set up
    G = []
    for v in range(len(graph)):
        G.append(v)
    current = source
    visited = [current]
    G.remove(current)

    # tie breakers on earliest node
    while len(visited) < len(graph):
        # grab nearest node from current
        min_dist = 10000
        minV = None
        for v in G: # loop through all unvisited nodes
            if graph[current][v] < min_dist and v not in visited:
                min_dist = graph[current][v]
                minV = v

        # visit the current node and remove it from G
        current = minV
        visited.append(current)
        G.remove(current)
        
    print(visited)


if __name__ == "__main__":
    graph = [[0, 2, 3, 2, 3, 5, 6], 
             [2, 0, 1, 4, 4, 5, 7],
             [3, 1, 0, 3, 4, 5, 9],
             [2, 4, 3, 0, 2, 4, 15],
             [3, 4, 4, 2, 0, 1, 9],
             [5, 5, 5, 4, 1, 0, 10],
             [6, 7, 9, 15, 9, 10, 0]]
    dijkstra(graph, 0)