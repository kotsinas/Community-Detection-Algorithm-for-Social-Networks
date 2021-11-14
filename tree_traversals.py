
class TreeNode:
    def __init__(self, node):
        self.nodeID = node
        self.right_link_value = None
        self.right_link_object = None
        self.right_thread = None
        self.left_thread = None
        self.left_link = None

    def add_right_child(self, next_element_of_the_list):

        # NON-RECURSIVE FUNCTION
        current = self
        while current is not None:
            if current.right_link_object:
                current = current.right_link_object

            else:
                current.right_link_object = next_element_of_the_list
                current.right_link_value = next_element_of_the_list.nodeID
                return

        # RECURSIVE FUNCTION
        '''if self.right_link_object:
            self.right_link_object.add_right_child(next_element_of_the_list)

        else:
            self.right_link_object = next_element_of_the_list
            self.right_link_value = next_element_of_the_list.nodeID'''

    def add_right_thread(self, root):
        self.right_thread = root

    def add_left_thread(self, j, w_ij, w_jroot, w_iroot):
        if (w_ij+w_jroot)/2 > w_iroot:
            self.left_thread = j

    def add_community(self, community):
        self.left_link = community

    def right_travers(self):

        # NON-RECURSIVE FUNCTION
        stack = list()
        current = self

        while True:
            if current is not None:
                stack.append(current)
                current = current.right_link_object

            else:
                return stack

        # RECURSIVE FUNCTION
        # elements = list()
        # elements.append(self)

        # if self.right_link_object:
            # elements += self.right_link_object.right_travers()

        # return elements

    def get_node_ids(self):

        # NON-RECURSIVE FUNCTION
        elements = list()
        current = self

        while True:
            if current is not None:
                elements.append(current.nodeID)
                current = current.right_link_object

            else:
                return elements

        # RECURSIVE FUNCTION
        # elements = list()
        # elements.append(self.nodeID)

        # if self.right_link_object:
            # elements += self.right_link_object.get_node_ids()

        # return elements


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


def get_subtree(tree, lt):
    subtree = []

    for node in tree.right_travers():
        subtree.append(node.nodeID)

        if node.nodeID == lt:
            return subtree


def path_sim(root, c):
    if root.nodeID in c:
        # the node already member of the target community
        return

    cur_path = []
    t_act = root
    active_list = set(root.get_node_ids())
    updates = 0
    length = 0.0

    for element in active_list:
        t_i = t_act.right_link_object

        if t_i is None:
            # the node cant be considered a member of the target community
            return
        else:
            if t_i.left_thread is not None:
                length = length + 1.3 + 1.2
                updates = updates + 2
                cur_path.append(t_act.nodeID)
                cur_path.append(t_i.left_thread)
                cur_path.append(t_i.nodeID)

                for node in t_i.left_link.right_travers():
                    if node.left_link is not None:
                        if node.nodeID == t_i.left_thread:
                            t_act = node
                            break

                s1 = set(t_i.left_link.get_node_ids())
                s2 = set(get_subtree(t_i, t_i.left_thread))
                active_list = s1.difference(set(cur_path), s2)

            else:
                length = length + 4.20
                updates = updates + 1
                cur_path.append(t_i.nodeID)
                t_i = t_act

                if t_i.left_link is not None:
                    s1 = set(t_i.left_link.get_node_ids())
                    active_list = s1.difference(set(cur_path))

        root = t_i

    if root.nodeID in c:
        path_strength = length/updates

        return path_strength, updates
    else:
        # the node cant be considered a member of the target community
        return


# Driver code
if __name__ == '__main__':

    # neighborhood = (1, {'9': 0.03, '7': 0.06, '77': 0.07, '88': 0.08, '8': 0.09, '2': 0.16, '3': 0.84, '6': 0.93})
    neighborhoods = [('A', {'E': 0.58, 'F': 0.77, 'J': 0.9, 'B': 0.96}), ('E', {'H': 0.56, 'A': 0.58, 'F': 0.82, 'I': 0.84}), ('F', {'A': 0.77, 'E': 0.82, 'G': 0.9}), ('I', {'H': 0.7, 'E': 0.84, 'G': 0.94}), ('G', {'H': 0.8, 'F': 0.9, 'I': 0.92}), ('B', {'A': 0.96, 'C': 1}), ('H', {'E': 0.56, 'I': 0.7, 'G': 0.8}), ('C', {'B': 1}), ('J', {'A': 0.9})]

    com = ['H', 'G', 'F', 'B', 'J']

    weight = 0.66

    dentra = []
    for node_nbr in neighborhoods:
        r = build_tree(node_nbr, weight)
        dentra.append(r)

    for tree in dentra:
        build_communities(tree, dentra)

    for tree in dentra:
        print(path_sim(tree, com))
