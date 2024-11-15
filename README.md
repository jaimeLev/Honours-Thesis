# Honours-Thesis
This thesis focuses on the development of the heuristic Zero Regret Model (ZRM) to solve the afternoon School Bus Routing Problem (SBRP).
We compare the ZRM to a revised implementation of Prim's greedy minimum spanning tree algorithm. We call this the Minimum Distance Model (MDM).

This repository contains the main code for the ZRM and the MDM, which can be found in capacitatedZeroRegret.py and capacitatedMinDistance.py respectively. These files individually can be run from the terminal without parameters to see the output of the mock suburb, or with parameters such as the busLoad, capacities and the random adjacency matrix. Note that the mock suburb is the same as presented in the thesis.

We have the script comparingModels.py which will run the ZRM and MDM for the parameters n and l, which are the number of bus stops, and the suburb size respectively.

The buildCapacities.py file contains the algorithm to randomise the bus stop capacities, and the randomAdjacencyMatrix.py file contains the algorithm to randomise the bus stop locations given n and l, and returns the adjacency matrix. These are spoken about in Section 3.1 of the thesis.

We also include the final spreadsheet of all results in AllResults.csv as well as some of the preliminary models constructed before the introduction of bus stop capacities and a busLoad, to show the Dijkstra working in the ZRM initially.
