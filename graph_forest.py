# graph_forest.py

import random
import visualiser_random_forest_graph as vr
import graph_helper as gh
import Classes as lp
from simulation import simulation


def provided_graph (matrix:int, color:list, firefighters: list,
                    fire:list, respawn:int, steps:int):
    '''
    Function that creates graph from given connections from a provided file.
    
    >>> example = [(0, 1), (2, 1), (3, 4), (5, 6), (5, 7), (7, 8),
                (8, 9), (9, 6), (3, 5), (4, 6), (2, 7)]
    >>> color = ["3"]
    >>> firefighters = 3
    >>> fire = [5, 30] # [ignition, transmission]
    >>> respawn = 5
    >>> steps = 20
    >>> provided_graph(example, color, firefighters, fire,
    respawn, steps)
    '''
    nodes = list(set().union(*matrix))

    #Check if the graph is planar
    if not gh.edges_planar(matrix):
        print("Graph is not planar, please change it.")
        return
    
    #Check if the graph is connected
    if not is_connected(matrix, nodes):
        print("Graph is not connected to itself, please change it.")
        return
    
    #Create the graph
    graph = vr.Visualiser(matrix,node_size=50)  
    
    #Dictionary with the connections of every node
    dict_nodes = dict_nodes_creator(matrix)

    
    skill = firefighters[1]
    firefighters = firefighters[0]
    F,ff_location = firefighters_location(skill, firefighters, nodes)
    
    nodes = list(set().union(*matrix))
    cmap, rmap = coloring_ratio(nodes, color)
    allnodes = cmap.copy()
    allnodes.update(rmap)
    allnodes = dict(sorted(allnodes.items()))

    '''
    allnodes -> every node on the graph
    cmap -> every node that is a tree with treestats
    rmap -> every node that is a rock
    '''

    graph.update_node_colours(cmap)
    graph.update_node_edges(ff_location)
    
    neighbor_location(allnodes, dict_nodes, ff_location)
    simulation(graph, cmap, rmap, respawn, firefighters,
               skill, fire, dict_nodes, ff_location, F, steps)
    
    vr.Visualiser.wait_close(graph)
    

def random_graph (matrix:int, color:list, firefighters: list,
                    fire:list, respawn:int, steps:int):
    '''
    Function that creates graph with random connections with a minimum number of nodes.
    
     >>> example = 10
    >>> color = ["3"]
    >>> firefighters = 3
    >>> fire = [5, 30] # [ignition, transmission]
    >>> respawn = 5
    >>> steps = 20
    >>> random_graph(example, color, firefighters, fire,
    respawn, steps)
    '''

    #generate the edges and possitions
    edgelist,pos = gh.voronoi_to_edges(matrix)  
    
    #Check if the graph is planar
    while gh.edges_planar(edgelist) == False:
        edgelist,pos = gh.voronoi_to_edges(matrix)

    #Dictionary with the connections of every node
    dict_nodes = dict_nodes_creator(edgelist) 

    #Create the graph
    graph = vr.Visualiser(edgelist,pos_nodes=pos,node_size=50)
    nodes = list(pos.keys())

    skill = firefighters[1]
    firefighters = firefighters[0]
    F,ff_location = firefighters_location(skill, firefighters, nodes)

    nodes = list(pos.keys())
    cmap, rmap = coloring_ratio(nodes, color) 
    allnodes = cmap.copy() 
    allnodes.update(rmap)
    allnodes = dict(sorted(allnodes.items())) 

    '''
    allnodes -> every node on the graph
    cmap -> every node that is a tree with treestats
    rmap -> every node that is a rock
    '''

    graph.update_node_colours(cmap)
    graph.update_node_edges(ff_location)
    
    neighbor_location(allnodes, dict_nodes, ff_location)
    simulation(graph, cmap, rmap, respawn, firefighters,
               skill, fire, dict_nodes,ff_location, F, steps)
    
    vr.Visualiser.wait_close(graph)
    
def coloring_ratio(edges: list, color_info: list):
    '''
    Function that gives colors for edges in a graph at the beginning of the simulation.
    Coloring pattern depends on the users choice. It returns cmap and rmap which are
    dictionaries with the nodes and their colors.
    >>> coloring_ratio({1:None, 2:None, 3:None}, ["2"])
    {1:0, 2:0, 3:0}
    '''
    cmap = {}
    rmap = {}
    if color_info[0] == "1":
        cmap= {i:random.randint(1,265) for i in random.sample(list(edges),int(len(edges)))}
    elif color_info[0] == "2":
        cmap= {i:random.randint(1,265) for i in random.sample(list(edges),int(0*len(edges)))}
    elif color_info[0] == "3":
        ratio = color_info[1] / 100
        cmap= {i:random.randint(1,265) for i in random.sample(list(edges),int(ratio*len(edges)))}
    cmap = dict(sorted(cmap.items()))
    rmap = [node for node in list(edges) if node not in cmap]
    rmap = {i: 0 for i in rmap}
    return cmap,rmap

def is_connected(connections:list, nodes:list):
    '''
    Check if graph is connected. Returns True if the graph is connected.
    >>>  is_connected([(0, 1),(1, 2),(2, 3),(3, 0)],[0,1,2,3])
    True
    '''
    G = {node: set() for node in nodes}
    for edge in connections:
        G[edge[0]].add(edge[1])
        G[edge[1]].add(edge[0])

    visited = set()
    stack = [next(iter(G))]

    while stack:
        node = stack.pop()
        visited.add(node)
        stack.extend(G[node] - visited)

    return len(visited) == len(nodes)

def dict_nodes_creator(edgelist):
    '''
    Function that creates a dictionary with the neighbors (conections) of each node.
    >>> edgelist = [(0, 1),(1, 2),(2, 3),(3, 0), (4, 3)]
    {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2, 4], 4: [3]}
    '''
    dict_nodes = {}
    for conection in edgelist:
        node1, node2 = conection
        if node1 not in dict_nodes:
            dict_nodes[node1] = []
        if node2 not in dict_nodes:
            dict_nodes[node2] = []
        dict_nodes[node1].append(node2)
        dict_nodes[node2].append(node1)
    return dict_nodes  

def firefighters_location(skill, firefighters, nodes):
    '''
    Function that defines how many firefighter objects are in the simulation,
    their skill and the location of each. It returns F(dictionary with firefighter objects
    and ff_location (list of the nodes with a firefighter).
    >>> skill = 30
    >>> firefighters = 4
    >>> nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    [0, 1, 5, 7]
    '''
    F = {}
    for i in range(firefighters):
        selected_node = random.choice(nodes)
        F[i] = lp.Firefighter(i, skill, selected_node)
        nodes.remove(selected_node)

    ff_location = []
    for i in range(firefighters):
        ff_location.append(F[i].current_patch)
    return F, ff_location

def neighbor_location(allnodes, dict_nodes, ff_location):
    '''
    Function that crates a dictionary with nodes and each landpatch object,
    defines if a landpatch object has a firefighter and
    defines the location of the neighbors of each node.
    >>> allnodes = {0: 0, 1: 104, 2: 137, 3: 151, 4: 242}
    >>> dict_nodes = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2, 4], 4: [3]}
    >>> ff_location = [0, 1]
    >>> neighbor_location(allnodes, dict_nodes, ff_location)
    '''
    L = {i:lp.Landpatch(i) for i in allnodes}
    for node_id, neighbors in dict_nodes.items():
        current_node = L[node_id]
        neighbor_instances = [L[neighbor_id] for neighbor_id in neighbors] 
        current_node.neighbors = neighbor_instances
    
    for patch_id in ff_location:
        if patch_id in L:
            L[patch_id].firefighter_present = True


if __name__ == "__main__":
    from User_interface import main_menu
    main_menu()


