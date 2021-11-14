import networkx as nx
import random
import time
import tree_traversals
import sys
# import json
sys.setrecursionlimit(10**6)


def sort_neighbors(d):
    new_dict = {}

    for e in d[1]:
        sub_dict = d[1][e]
        for d2 in sub_dict:
            # print(sub_dict[d2])
            new_dict.update({e: sub_dict[d2]})

    new_dict = dict(sorted(new_dict.items(), key=lambda kv: kv[1]))
    return d[0], new_dict


def count_set_bits(b):
    count = 0
    while b:
        count += b & 1
        b >>= 1
    return count


def str_bitwise_xor(array, t):
    result = ""
    max_len = -1
    for i in range(t):
        max_len = max(max_len, len(array[i]))
        array[i] = arr[i][::-1]

    for i in range(t):
        s = ""
        for j in range(max_len - len(arr[i])):
            s += "0"

        arr[i] = arr[i] + s

    for i in range(max_len):
        pres_bit = 0

        for j in range(t):
            pres_bit = pres_bit ^ (ord(arr[j][i]) - ord('0'))

        result += chr(pres_bit + ord('0'))

    result = result[::-1]
    return result


def rand_key(p):
    p = p - 3

    key1 = ""
    for a in range(p):
        temp = str(random.randint(0, 1))
        key1 += temp
    return '111'+key1


def ncd(t):
    # network connectivity degree for every node of the network
    count = 0
    s = 0.0

    for user in t[1]:
        s += t[1][user]
        count += 1

    return s/count


def compute_acc(circle_, n_hoods):
    # returns (community id, number of members, average community connectivity)
    id_ = circle_[0]
    # circle_.pop(0)
    s = 0.0
    count = 1

    for j in range(1, len(circle_)):

        for n_hood in n_hoods:

            if circle_[j] == n_hood[1][0]:
                s += n_hood[0]
                count += 1

    if count != 0:
        return id_, count, s/count


def dia(circle_, graph):

    circle_.pop(0)
    q = nx.Graph()

    for o in circle_:
        q.add_node(o)

    for (j, p, w) in graph.edges.data('weight'):

        if j in q.nodes:
            if p in q.nodes:
                q.add_weighted_edges_from([(j, p, w)])

    if len(circle_) == 0:
        pass
    else:
        if nx.is_connected(q):
            return nx.diameter(q)+5
        else:
            return 3


def declare_membership(path_sim_t, diam, acc):
    # path_sim_t = (path_strength, updates)
    # diam = diameter
    # acc = average community connectivity

    if path_sim_t[1] <= diam+5:
        if path_sim_t[0] >= acc-1:
            return 'the node can be considered a member of the target community'
        else:
            return


if __name__ == '__main__':
    start = time.perf_counter()
    with open('social_network_samples\\0.edges', 'r') as fh:
    # with open('C:\\Users\\kots\\Desktop\\0.edges', 'r') as fh:
        # new_file = fh.read()
        # new_file = new_file.replace(',', ' ')
        # print(new_file)
        g = nx.read_edgelist(fh, delimiter=' ', create_using=nx.Graph(), nodetype=str)

    # g = nx.read_edgelist('C:\\Users\\giorgos\\Desktop\\twitter_combined.txt', create_using=nx.Graph(), nodetype=str)
    # print(nx.info(g))
    print('Origin of the graph: Facebook')
    print('Number of nodes:', g.number_of_nodes())
    print('Density of the graph:', format(nx.density(g), '.4f'))
    # print('Features in common: 3 (at least)')

    circles = []
    binary_values = {}
    features = 10
    with open('social_network_samples\\0.circles', 'r') as f:
    # with open('C:\\Users\\kots\\Desktop\\0.circles', 'r') as f:
        for line in f:
            k = line.split()
            circles.append(k)
            c = f.readline().split('\t')# Driver code
            # print(c)
            c[-1] = c[-1].strip('\n')
            circles.append(c)

    # music communities
    '''music1 = ['Folk']
    music2 = ['Techno/House']
    with open('C:\\Users\\giorgos\\Desktop\\HU_genres.json', 'r') as f:
        data = json.load(f)

    for key, value in data.items():
        # print(key, '-->', value)
        for kind in value:
            if kind == 'Folk':
                music1.append(key)
            elif kind == 'Techno/House':
                music2.append(key)
    circles.append(music1)
    circles.append(music2)'''

    w = 0.66
    for i in g.nodes:
        binary_values[i] = rand_key(features)
    # print(binary_values)

    for (u, v) in g.edges():
        arr = [binary_values[u], binary_values[v]]
        XOR = str_bitwise_xor(arr, 2)
        number_of_1s = count_set_bits(int(XOR, 2))
        weigh = number_of_1s/features
        g.add_weighted_edges_from([(u, v, weigh)])
        # print(f"({u}, {v}, {weigh:.3})")

    neighborhoods = []

    for n in g.adjacency():
        # print(sort_neighbors(n))
        # print(ncd(sort_neighbors(n)))
        element = (ncd(sort_neighbors(n)), sort_neighbors(n))
        # print(element)
        neighborhoods.append(element)

    diameters = {}
    # diameters = {id: diameter, ...}
    comm = []
    # comm = [(community id, number of members, average community connectivity), ...()]
    for circle in circles:
        comm.append(compute_acc(circle, neighborhoods))
        diameters.update({circle[0]: dia(circle, g)})

    for _ in comm:
        pass
        # print(_)

    for _ in diameters.items():
        pass
        # print(_)

    target_com = circles[11]
    d = diameters['circle11']
    a = comm[11][2]

    trees = []
    for node in neighborhoods:
        r = tree_traversals.build_tree(node[1], w)
        trees.append(r)

    for tree in trees:
        tree_traversals.build_communities(tree, trees)

    stronger_paths = []
    for tree in trees:
        stronger_paths.append(tree_traversals.path_sim(tree, target_com))

    s = 0
    for path in stronger_paths:
        if path is not None:
            if declare_membership(path, d, a) is not None:
                s = s + 1
            # print(path)
            # print(declare_membership(path, d, a))

    print('Nodes that can be considered members of the target community:', s)

    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} seconds')
    # end
