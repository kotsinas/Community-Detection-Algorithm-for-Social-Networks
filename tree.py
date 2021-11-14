class TreeNode:
    def __init__(self, node):
        self.nodeID = node
        self.right_link_value = None
        self.right_link_object = None
        self.right_thread = None
        self.left_thread = None
        self.left_link = None

    def add_right_child(self, next_element_of_the_list):

        if self.right_link_object:
            self.right_link_object.add_right_child(next_element_of_the_list)

        else:
            self.right_link_object = next_element_of_the_list
            self.right_link_value = next_element_of_the_list.nodeID

    def add_right_thread(self, root):
        self.right_thread = root

    def add_left_thread(self, j, w_ij, w_jroot, w_iroot):
        if (w_ij+w_jroot)/2 > w_iroot:
            self.left_thread = j

    def add_community(self, community):
        self.left_link = community

    def right_travers(self):
        elements = list()
        elements.append(self)

        if self.right_link_object:
            elements += self.right_link_object.right_travers()

        return elements

    def get_node_ids(self):
        elements = list()
        elements.append(self.nodeID)

        if self.right_link_object:
            elements += self.right_link_object.get_node_ids()

        return elements


def build_tree(sorted_list, edge):

    root = TreeNode(sorted_list[0])

    neighbor_list = [(k, v) for k, v in sorted_list[1].items()]
    # print(neighbor_list)
    m = len(neighbor_list)

    for i in range(m):
        node = TreeNode(neighbor_list[i][0])
        node.add_right_thread(sorted_list[0])
        root.add_right_child(node)
        for j in range(i+1, m):
            node.add_left_thread(neighbor_list[j][0], edge, neighbor_list[j][1], neighbor_list[i][1])
            break

    return root


def build_communities(tree, trees):
    for node in tree.right_link_object.right_travers():
        for t in trees:
            if node.nodeID == t.nodeID:
                node.add_community(t.right_link_object)


# Driver code
if __name__ == '__main__':

    # neighborhood = (1, {'9': 0.03, '7': 0.06, '77': 0.07, '88': 0.08, '8': 0.09, '2': 0.16, '3': 0.84, '6': 0.93)
    neighborhoods = [(0.1, ('A', {'E': 0.58, 'F': 0.77, 'J': 0.9, 'B': 0.96})), (0.2, ('E', {'H': 0.56, 'A': 0.58, 'F': 0.82, 'I': 0.84})), (0.7, ('F', {'A': 0.77, 'E': 0.82, 'G': 0.9})), (0.8, ('I', {'H': 0.7, 'E': 0.84, 'G': 0.94})), (0.7,('G', {'H': 0.8, 'F': 0.9, 'I': 0.92})), (0.8, ('B', {'A': 0.96, 'C': 1}))]

    weight = 0.66

    dentra = []
    for node_nbr in neighborhoods:
        r = build_tree(node_nbr[1], weight)
        dentra.append(r)

    for tree in dentra:
        build_communities(tree, dentra)

    # testing trees
    for tree in dentra:
        # root and the right tree
        print('tree with:')
        print('root =', tree.nodeID, 'right subtree--->', tree.right_link_object.get_node_ids())

        # right thread pointing to the root
        '''for node in tree.right_link_object.right_travers():
            print('node.s', node.nodeID, 'right thread points-->', node.right_thread)
        print()'''

        # left thread pointing to a child as described in the paper
        '''for node in tree.right_link_object.right_travers():
            if node.left_thread is not None:
                print('node.s', node.nodeID, 'left thread points-->', node.left_thread)'''

        # left link communities of the children
        for node in tree.right_link_object.right_travers():
            if node.left_link is not None:
                print('node.s', node.nodeID, 'left link community =', node.left_link.get_node_ids())




