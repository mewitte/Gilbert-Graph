import logging
import math
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
import random
import sys

class RandomGraph:
  def __init__(self, n, p):
    self._create_random_graph(n, p)
    if not nx.is_connected(self._random_graph):
      sys.stderr.write("Graph is not connected!")
      exit(1)
    self._compute_average_path_length()
    self._compute_clustering_coefficient()
    self._compute_average_degree()
    
  def _create_random_graph(self, n, p):
    self._random_graph = nx.Graph()
    self._random_graph.add_nodes_from(range(0, n))
    for i in self._random_graph.nodes:
      for j in self._random_graph.nodes:
        if i != j and random.random() < p:
          self._random_graph.add_edge(i, j)

  def _get_sample_paths(self):
    node_count = len(self._random_graph)
    sample_paths = []
    if node_count <= 14: # with 14 nodes, there are a maximum of 91 node combinations possible, 15 has 105
      for node1 in list(self._random_graph.nodes):
        for node2 in list(self._random_graph.nodes):
          if (
            node1 != node2
            and (node1, node2) not in sample_paths
            and (node2, node1) not in sample_paths
          ):
            sample_paths.append((node1, node2))
    else:
      while len(sample_paths) < 100:
        random_node1 = list(self._random_graph.nodes)[random.randint(0, node_count - 1)]
        random_node2 = list(self._random_graph.nodes)[random.randint(0, node_count - 1)]
        if (
          random_node1 != random_node2
          and (random_node1, random_node2) not in sample_paths
          and (random_node2, random_node1) not in sample_paths
        ):
          sample_paths.append((random_node1, random_node2))
    return sample_paths

  def _compute_average_path_length(self):
    sample_paths = self._get_sample_paths()
    distances = []
    for (first_node, second_node) in sample_paths:
      distances.append(nx.shortest_path_length(self._random_graph, first_node, second_node))
    self.average_path_length = sum(distances) / len(distances)

  def _compute_node_clustering_coefficients(self):
    for node in list(self._random_graph.nodes):
      triangles = 0
      neighbor_pairs = 0
      neighbors = list(self._random_graph.neighbors(node))
      for neighbor1 in neighbors:
        for neighbor2 in neighbors:
          if neighbor1 == neighbor2:
            continue
          neighbor_pairs += 1
          if self._random_graph.has_edge(neighbor1, neighbor2):
            triangles += 1
      self._random_graph.nodes[node]["clustering_coefficient"] = triangles / neighbor_pairs

  def _compute_clustering_coefficient(self):
    self._compute_node_clustering_coefficients()
    clustering_coefficients = []
    for (_, coefficient) in list(self._random_graph.nodes.data("clustering_coefficient")):
      clustering_coefficients.append(coefficient)
    self.clustering_coefficient = sum(clustering_coefficients) / len(clustering_coefficients)

  def _compute_average_degree(self):
    degrees = []
    for (_, degree) in list(self._random_graph.degree):
      degrees.append(degree)
    self.average_degree = sum(degrees) / len(degrees)

  def get_average_path_length(self):
    return nx.average_shortest_path_length(self._random_graph)

  def get_clustering_coefficient(self):
    return nx.average_clustering(self._random_graph)

if __name__ == "__main__":
  directory = sys.argv[1]
  Path(f"./{directory}").mkdir(parents=True, exist_ok=True)
  logging.basicConfig(
    filename=f"./{directory}/gg.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
  )
  n = 32
  p = 0.3
  path_lengths = []
  nodes = []
  for c in range(0, 20):
    logging.info(f"Creating graph with n={n} and p={p}")
    graph = RandomGraph(n, p)
    logging.info(f"Average degree: {graph.average_degree}")
    logging.info(f"Average path length: {graph.average_path_length}")
    logging.info(f"Clustering coefficient: {graph.clustering_coefficient}")
    nodes.append(n)
    path_lengths.append(graph.average_path_length)
    p = p * (n-1) / (n*2 - 1)
    n = n*2
  plt.plot(nodes, path_lengths)
  plt.xlabel("Number of nodes")
  plt.ylabel("Average path length")
  plt.savefig(f"./{directory}/path_lengths.png")
