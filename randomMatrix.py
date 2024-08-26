import random

def generateRandomMatrix(n):
    length = n
    print(length)
    locations = [(0,0)]
    sign = [-1,1]
    for i in range(n):
        location = (random.randint(0, length)*random.choice(sign), random.randint(0, length)*random.choice(sign))
        while location in locations:
            location = (random.randint(0, length)*random.choice(sign), random.randint(0, length)*random.choice(sign))
        locations.append(location)

    print(locations)


    # do manhattan distances from bus stop to school
    distances = [abs(location[0]) + abs(location[1]) for location in locations]
    print(distances)
    manhattanMatrix = []
    for node0 in locations:
        distanceRow = []
        for node1 in locations:
            if node0 == node1:
                distanceRow.append(0)
            else:
                distanceRow.append(abs(node1[0] - node0[0]) + abs(node1[1] - node0[1]))
        manhattanMatrix.append(distanceRow)
    return manhattanMatrix




    # create manhattan distane matrix
if __name__ == "__main__":
    n = 6
    busLoad = 10
    distanceMatrix = generateRandomMatrix(n)
    with open('randomMatrix.txt', 'w') as file:
        for i in distanceMatrix:
            file.write(str(i) + "\n")
    capacities = [0]
    for i in range(n):
        capacities.append(random.randint(1,int(n/2) + 1))
    with open('capacities.txt', 'w') as file:
        file.write(str(capacities))
    print(capacities, " capacities")