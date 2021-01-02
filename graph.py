import copy
import numpy as np
import random

def diff_list(L1, L2):
    """
    Parameters:
        L1(list)
        L2(list)
    
    Returns:
        L1 - L2
    """
    result = [v for v in L1 if v not in L2]
    return result

def matrice_to_graph(filename):
    """
    Parameters:
        filename(string): name of the file where the matrix T is stored
    
    Returns:
        dictionary: key = product's idea / value = list of neighbours
    """

    dict_graph = {}

    with open(filename, "r") as f:
        nb = int(f.readline())
        for i in range(nb):
            tmp = []
            line = f.readline().split("\t")
            for j in range(nb):
                if int(line[j]) == 1 and i != j:
                    tmp.append(j)
            dict_graph[i] = tmp

    return dict_graph

def set_seed_random(seed):
    """
    Parameters:
        seed(int): int to initialize the generator with
    """
    random.seed(seed)

def get_random_edge(graph):
    v1 = random.choice(list(graph.keys()))
    v2 = random.choice(graph[v1])
    return (v1, v2)


def include(res, U, edge):
    v1 = edge[0]
    v2 = edge[1]
    
    if res == []:
        res.append([v1, v2])
        return res

    if v1 in U and v2 in U:
        for i in res:
            if v1 in i and v2 in i:
                break
            if v1 in i:
                for j in res:
                    if v2 in j:
                        i.extend(j)
                        res.remove(j)
                        break
        return res
    
    if v1 not in U and v2 not in U:
        res.append([v1, v2])
        return res 
    
    if v1 in U and v2 not in U:
        for i in res:
            if v1 in i:
                i.append(v2)
                break 

        return res
    
    if v2 in U and v1 not in U:
        for i in res:
            if v2 in i:
                i.append(v1)
                break
        
        return res 

def contract_edge(graph, edge):
    v1 = edge[0]
    v2 = edge[1]

    # ajout des voisins de v2 aux voisins de v1
    for edge in graph[v2]:
        if edge != v1:
            graph[v1].append(edge)   

    # suppression de v2 dans le dictionnaire graph[voisin_de_v2]
    # et ajout de v1 dans les voisins des voisins de v2        
    for edge in graph[v2]:
        graph[edge].remove(v2)
        if edge != v1:
            graph[edge].append(v1)   
    # suppression du noeud v2 dans le graphe
    del graph[v2]

    return graph

def krager(graph, r):
    """
    Parameters:
        graph(dict): key: node / value: list of neighbours of key
        r(int): number of providers

    Returns:
        list of keys of the contracted graph + size of cut 
    """
    res = []
    U = []
    while(len(graph) > r):
        edge = get_random_edge(graph)
        res = include(res, U, edge)
        #print("chosen edge: " + str(edge))
        #print(res)
        if edge[0] not in U: 
            U.append(edge[0])
        if edge[1] not in U:
            U.append(edge[1])
        graph = contract_edge(graph, edge)

    for u in diff_list(list(graph.keys()), U):
        res.append([u])

    mincut = len(graph[list(graph.keys())[0]])
    
    return list(graph.keys()), res, mincut
    #return list(graph.keys()), mincut


def repe_krager(graph, r, k, seed=None):
    """
    Parameters:
        graph(dict): key: node / value: list of neighbours of key
        r(int): number of providers
        k(int): number of repetitions

    Returns: 

    """

    if seed:
        set_seed_random(seed)

    list_graph_keys = []
    mincuts = []
    partitions = []

    for i in range(k):
        print("RÉPÉTITION " + str(i+1))
        graph_copy = copy.deepcopy(graph)
        list_graph_key, part, mincut = krager(graph_copy, r)
        list_graph_keys.append(list_graph_key)
        mincuts.append(mincut)
        partitions.append(part)

    arr = np.array(mincuts)
    best_mincut = np.min(mincuts)
    i_best_mincut = np.argmin(arr)
    best_graph = list_graph_keys[i_best_mincut]
    best_partition = partitions[i_best_mincut]
    print(mincuts)

    return best_mincut, best_graph, best_partition, mincuts

def get_edge(B):
    """
    Parameters:
        B(list)
    
    Returns:
        edge(v1, v2)
    """
    index_arr = np.array([i for i in range(len(B)*len(B))])
    proba = np.array(B).flatten()
    proba = proba / proba.sum(axis=0, keepdims=1)
    index = np.random.choice(index_arr, p=proba)
    i = index//len(B)
    j = index%len(B)
    print("choosen edge: B[" + str(i) + "][" + str(j) + "] = " + str(B[i][j]))
    return (i, j)


def contract_edge2(B, graph, edge):
    v1 = edge[0]
    v2 = edge[1]

    # ajout des voisins de v2 aux voisins de v1
    for edge in graph[v2]:
        if edge != v1:
            graph[v1].append(edge)   

    # suppression de v2 dans le dictionnaire graph[voisin_de_v2]
    # et ajout de v1 dans les voisins des voisins de v2        
    for edge in graph[v2]:
        graph[edge].remove(v2)
        if edge != v1:
            graph[edge].append(v1)   
    # suppression du noeud v2 dans le graphe
    del graph[v2]

    for i in range(len(B)):
        if i != v1 and B[v1][i] < B[v2][i]:
            B[v1][i] = B[v2][i]
            B[i][v1] = B[v1][i]
        B[v2][i] = 0
        B[i][v2] = 0        

    return B, graph


def krager2(B, graph, r):
    res = []
    U = []
    while(len(graph) > r):
        edge = get_edge(B)
        (v1, v2) = edge
        res = include(res, U, edge)
        if v1 not in U:
            U.append(v1)
        if v2 not in U:
            U.append(v2)
        B, graph = contract_edge2(B, graph, edge)

    for u in diff_list(list(graph.keys()), U):
        res.append([u])

    mincut = len(graph[list(graph.keys())[0]])

    return list(graph.keys()), res, mincut

def repe_krager2(B, graph, r, k, seed=None):
    if seed:
        set_seed_random(seed)

    list_graph_keys = []
    mincuts = []
    partitions = []

    for i in range(k):
        print("RÉPÉTITION " + str(i+1))
        graph_copy = copy.deepcopy(graph)
        B_copy = copy.deepcopy(B)
        list_graph_key, part, mincut = krager2(B_copy, graph_copy, r)
        list_graph_keys.append(list_graph_key)
        mincuts.append(mincut)
        partitions.append(part)

    arr = np.array(mincuts)
    best_mincut = np.min(mincuts)
    i_best_mincut = np.argmin(arr)
    best_graph = list_graph_keys[i_best_mincut]
    best_partition = partitions[i_best_mincut]

    return best_mincut, best_graph, best_partition, mincuts
