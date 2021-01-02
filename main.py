import copy
import graph
import numpy as np 
import product 
import provider 
import sys

r = 3
N = 100
repe = 20
seeds = [1, 3, 5, 8, 10]

filename_products = "products0.txt"
filename_T = "T_matrix0.txt"

if len(sys.argv) != 2:
    print("Pass the question in argument please")
    print("Example: python ./main.py 1")
    print("to test the question 1")
    exit(1)

q = int(sys.argv[1])

############## QUESTION 1 ##############
if q == 1:
    print("EXECUTING QUESTION 1")
    list_providers = provider.feed_providers(r)
    list_products = product.feed_products(list_providers, N)
    product.write_products("products_big.txt", list_products)
    T = product.feed_T_matrice(list_products)
    product.write_matrice("T_matrix_big.txt", T)

############## QUESTION 2 ##############
if q == 2:
    print("EXECUTING QUESTION 2")
    dict_products = product.get_products(filename_products)


############## QUESTION 3 ##############
if q == 3:
    print("EXECUTING QUESTION 3: Nothing to do")

############## QUESTION 4 ##############
if q == 4:
    print("EXECUTING QUESTION 4")
    g = graph.matrice_to_graph(filename_T)
    g_copy = copy.deepcopy(g)
    best_mincut, best_graph, best_partition, mincuts = graph.repe_krager(g_copy, r, repe)


############## QUESTION 5 ##############
if q == 5:
    print("EXECUTING QUESTION 5: Nothing to do")

############## QUESTION 6 ##############
if q == 6:
    g = graph.matrice_to_graph(filename_T)
    for seed in seeds:
        print("EXECUTING QUESTION 6")
        g_copy = copy.deepcopy(g)
        best_mincut, best_graph, best_partition, mincuts = graph.repe_krager(g_copy, r, repe, seed)
        print("\n\nBEST MINCUT = " + str(best_mincut))
        print("\nMINCUTS: " + str(mincuts))
        print("\nBEST PARTITION: " + str(best_partition))

############## QUESTION 7 ##############
if q == 7:
    print("EXECUTING QUESTION 7: Nothing to do")

############## QUESTION 8 ##############
if q == 8:
    print("EXECUTING QUESTION 8")
    list_providers = provider.feed_providers(r)
    list_products = product.feed_products(list_providers, N)
    T = product.read_matrice_from_file(filename_T)
    B = product.feed_B_matrice(T)
    product.write_matrice("B_matrix0.txt", B)
    g = graph.matrice_to_graph(filename_T)
    best_mincut, best_graph, best_partition, mincuts = graph.repe_krager2(B, g, r, repe)
    print("\n\nBEST MINCUT = " + str(best_mincut))
    print("\nMINCUTS: " + str(mincuts))
    print("\nBEST PARTITION: " + str(best_partition))