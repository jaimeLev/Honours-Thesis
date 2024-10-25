import random

# This function randomises the number of students at each bus stop
# ie. the bus stop capacities c_i for i = {1,...,n} where n = # bus stops
# The bus load is set to 64 for this investigation
# To generate the desires bus stop capacities, change line 11 to say <n>stopCapacities.txt
# and update lines 13, 14, 15 and 17 by the instructions on the line

smallest = float('inf')
largest = 0
with open("capacities/128stopCapacities.txt", "w") as f:
    for j in range(100):
        arr = [1]*128 # vary for number of bus stops n = 8, 16, 32, 64, 128
        for i in range(72): # vary this from 200 - n
            index = random.randint(0,127) # 0 to (n-1)
            while arr[index] >= 32: # stops bus stop capacity c_i exceeding half bus load 64
                index = random.randint(0,127) # 0 to (n-1)
            arr[index] += 1
        f.write(str(arr)+"\n")
        if min(arr) < smallest:
            smallest = min(arr)
        if max(arr) > largest:
            largest = max(arr)
    print(smallest)
    print(largest)
