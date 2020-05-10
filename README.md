# Gilbert-Graph

## Installation
* `sudo apt install python3 python3-pip`
* `pipenv install`

## Usage
To create a Gilbert random graph, just call `RandomGraph(n, p)`. The average path length will then be saved as `graph.average_path_length`, the clustering coefficient will be saved as `graph.clustering_coefficient`. For comparison, you can call `graph.get_average_path_length()` and `graph.get_clustering_coefficient()`, which calls the NetworkX alogrithms for the problem. Note that for big values for n, getting the average path length will take some time.
