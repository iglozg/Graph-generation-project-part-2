# simulation.py

import random
import Classes as lp
from Reporting import plotting

def simulation(graph, cmap, rmap, respawn, firefighters, skill, fire, dict_nodes, ff_location, F, steps):
    '''
    Function that updates the graph and plots trees population, non combustible land and wildfires.
    '''
    transmission = fire[1] # Probability of fire to spread to adyacent nodes
    ignition = fire[0] # Probability of a treepatch to generate a wildfire
    nodes_t = cmap.copy() # Every node that is a tree without fire
    nodes_f = {} # Every node that is a tree with fire
    T = {i: lp.Treepatch(i, cmap[i]) for i in cmap} # Dictionary of Treepatch objects
    R = {i:lp.Rockpatch(i) for i in rmap} # Dictionary of Rockpatch objects
    wood = [len(cmap.keys())]
    rock = [len(rmap.keys())]
    fire = [0]
    for i in range(1, steps + 1): # Each time the loop is executed is a step.

        for j in nodes_t: # Each treepatch without wildfire increases treestats by 10
            T[j].updateland('nofire')
            cmap[j] = T[j].treestats

        fcolor = cmap.copy() # color update
        for key in cmap.keys() & nodes_f.keys():
            if fcolor[key] == nodes_f[key]:
                fcolor[key] -= 256
        graph.update_node_colours(fcolor)
        
        rmap1=rmap.copy()
        for j in rmap1: # Each Rockpatch has a probability to become a Treepatch
            rn = respawn_number(respawn)
            if rn == 2:
                R[j].mutate(lp.Treepatch(j,50))
                T[j] = lp.Treepatch(j,50)
                cmap[j] = T[j].treestats
                del R[j]
                del rmap[j]
        cmap=dict(sorted(cmap.items()))
        nodes_t=dict(sorted(nodes_t.items()))
        T=dict(sorted(T.items()))

        fcolor = cmap.copy() # color update
        for key in cmap.keys() & nodes_f.keys():
            if fcolor[key] == nodes_f[key]:
                fcolor[key] -= 256
        graph.update_node_colours(fcolor)
        
        tn = transmission_number(transmission)
        if tn == 2: # Each Treepatch with wildfire has a probability to spread to adyacen Treepatches
            trans_nodes = [val for key in nodes_f.keys() for val in dict_nodes[key]]
            trans_nodes.sort()
            trans_nodes = {key: cmap[key] for key in trans_nodes if key in cmap}
            nodes_t = {key: value for key, value in nodes_t.items() if key not in trans_nodes}
            nodes_f.update(trans_nodes)
            nodes_f=dict(sorted(nodes_f.items()))
        

        fcolor = cmap.copy() # color update
        for key in cmap.keys() & nodes_f.keys():
            if fcolor[key] == nodes_f[key]:
                fcolor[key] -= 256
        graph.update_node_colours(fcolor)
        
        for j in list(nodes_t): # Each treepatch has a probability to create a wildfire
            ig = ignition_number(ignition)
            if ig == 2:
                nodes_f[j] = T[j].treestats
                del nodes_t[j]

        nodes_f=dict(sorted(nodes_f.items()))
        
        fcolor = cmap.copy() # color update
        for key in cmap.keys() & nodes_f.keys():
            if fcolor[key] == nodes_f[key]:
                fcolor[key] -= 256
        graph.update_node_colours(fcolor)

        nodes_f1 = nodes_f.copy()
        for f in range(firefighters): # Each loop iteration is one firefighter
            if F[f].current_patch in nodes_f: # If the location of the firefighter is burning, he stays
                F[f].busy = True # Firefighter is extinguishing a wildfire
                sk = skill_number(skill)
                if sk == 2:
                    del nodes_f[F[f].current_patch]
                    nodes_t[F[f].current_patch] = cmap[F[f].current_patch]
            else: 
                F[f].busy = False # Firefighter is not extinguishing a wildfire
                neighbor_nodes = dict_nodes[F[f].current_patch]
                neighbor_nodes = [x for x in neighbor_nodes if x not in ff_location]
                matching_nodes = [node for node in neighbor_nodes if node in nodes_f]
                if neighbor_nodes: # If an adyacent node is on fire, he moves to them
                    if matching_nodes:
                        selected_node = random.choice(matching_nodes)
                        F[f].busy = True
                        sk = skill_number(skill)
                        if sk == 2:
                            del nodes_f[selected_node]
                            nodes_t[selected_node] = cmap[selected_node]
                    else: # If there is not adyacent node on fire, he moves randomly to a patch
                        selected_node = random.choice(neighbor_nodes)
                    ff_location.remove(F[f].current_patch)
                    F[f].current_patch = selected_node 
                    ff_location.insert(0, selected_node)

        nodes_t=dict(sorted(nodes_t.items()))

        graph.update_node_edges(ff_location) # firefighters location are updated
        fcolor = cmap.copy()
        for key in cmap.keys() & nodes_f.keys(): # update colors
            if fcolor[key] == nodes_f[key]:
                fcolor[key] -= 256

        nodes_f1 = nodes_f.copy()
        for n in nodes_f1: # if a Treepatch is on fire, its treestats are reduced by 20
            T[n].updateland('fire')
            if (T[n].treestats) <= 0:
                T[n].mutate(lp.Rockpatch(n))
                R[n] = lp.Rockpatch(n)
                rmap[n] = 0
                del T[n]
                del cmap[n]
                del nodes_f[n]
            else:
                cmap[n] = T[n].treestats
                nodes_f[n] = T[n].treestats

        cmap=dict(sorted(cmap.items()))
        rmap=dict(sorted(rmap.items()))
        nodes_f=dict(sorted(nodes_f.items()))
        R=dict(sorted(R.items()))

        fcolor = cmap.copy()
        for key in cmap.keys() & nodes_f.keys(): # color update
            if fcolor[key] == nodes_f[key]:
                fcolor[key] -= 256
        
        
        fires=list(fcolor.values())
        for land in fires: 
            if land >= 0:
                fires.remove(land)
            else:
                continue
        wood.append(len(cmap))
        rock.append(len(rmap))
        fire.append(len(fires))
     
        graph.update_node_colours(fcolor)
    plotting(wood, rock, fire)

def ignition_number(ignition:int):
    '''
    Function that returns randomly 1 or 2 depending on the probability decided by the user.
    '''
    if random.uniform(0, 1) > (ignition/100):
        return 1
    else:
        return 2

def transmission_number(transmission:int):
    '''
    Function that returns randomly 1 or 2 depending on the probability decided by the user.
    '''
    if random.uniform(0, 1) > (transmission/100):
        return 1
    else:
        return 2

def skill_number(skill:int):
    '''
    Function that returns randomly 1 or 2 depending on the probability decided by the user.
    '''
    if random.uniform(0, 1) > (skill/100):
        return 1
    else:
        return 2
        
def respawn_number(respawn:int):
    '''
    Function that returns randomly 1 or 2 depending on the probability decided by the user.
    '''
    if random.uniform(0, 1) > (respawn/100):
        return 1
    else:
        return 2
