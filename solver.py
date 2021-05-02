import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob

# takes in a graph G and returns the number of cities that can be removed and 
# the number of edges that can be removed (k, c)
def find_params(G):
    n = nx.number_of_nodes(G)
    if 20 <= n <= 30:
        return (15, 1)
    if 31 <= n <= 50:
        return (50, 3)
    if 51 <= n <= 100:
        return (100, 5)

# Removes the edge in G that will increase the length of the shortest s-t path the most. 
# returns the edge if an edge was removed, and returns None otherwise.
def remove_edge(G, t, k):
    max_edge = None
    max_score = 0
    shortest = nx.dijkstra_path(G, 0, t, weight='weight')
    for i in range(0, len(shortest) - 1):
        curr = (shortest[i], shortest[i + 1])
        if is_valid_solution(G, [], [curr], t):
            temp_score = calculate_score(G, [], [curr], t)
            if temp_score > max_score:
                max_score = temp_score
                max_edge = curr
    if not (max_edge is None):
        k.append(max_edge)
        G.remove_edges_from([max_edge])
    return max_edge

def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    c = [] # list of cities to remove
    k = [] # list of edges to remove
    t = nx.number_of_nodes(G) - 1 
    e, v = find_params(G) 
    H = G.copy()
    # Handles removing nodes
    while v:
        max_city = None
        max_score = 0
        shortest = nx.dijkstra_path(H, 0, t, weight='weight') # get the shortest path from s to t
        for i in range(1, len(shortest) - 1): # iterate through nodes in the shortest path
            curr = shortest[i]
            if is_valid_solution(H, [curr], [], t):
                temp_score = calculate_score(H, [curr], [], t)
                if temp_score > max_score:
                    max_score = temp_score
                    max_city = curr
        if max_city is None:
            removed_e = remove_edge(H, t, k)
            if removed_e is None:
                break
            else:
                e -= 1
        else:
            c.append(max_city)
            H.remove_nodes_from([max_city])
            v -= 1
    
    # Handles removing edges
    while e:
        removed_e = remove_edge(H, t, k)
        if removed_e is None:
            break
        else:
            e -= 1
    return c, k


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    c, k = solve(G)
    t = nx.number_of_nodes(G) - 1
    assert is_valid_solution(G, c, k, t)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k, t)))
    write_output_file(G, c, k, 'outputs/small-1.out')


# # # For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     dirs = ['small', 'medium', 'large']
#     for d in dirs:
#         inputs = glob.glob('inputs/' + d + '/*')
#         for input_path in inputs:
#             output_path = 'outputs/' + d + '/' + basename(normpath(input_path))[:-3] + '.out'
#             G = read_input_file(input_path)
#             t = nx.number_of_nodes(G) - 1
#             c, k = solve(G)
#             assert is_valid_solution(G, c, k, t)
#             distance = calculate_score(G, c, k, t)
#             write_output_file(G, c, k, output_path)
