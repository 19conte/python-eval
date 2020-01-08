class Node():
    
    def __init__(self, char, wgt):
        self.char = char
        self.wgt = wgt
        self.child1 = None
        self.child2 = None

    def __eq__(self, other):
        if(other == None):
            return False
        if(not isinstance(other, Node)):
            return False
        return self.wgt == other.wgt

    def __lt__(self, other):
        return self.wgt < other.wgt
        

class TreeBuilder():

    def __init__(self, text):
        self.text = text
        self.Leaf_queue = []
        self.Internal_queue = []

    def weight_dict(self):  
        """ Creates a dictionnary with the weight of each character """

        weight = {}
        for character in self.text:
            if not character in weight:
                 weight[character] = 0
            weight[character] += 1
        return weight

    @staticmethod
    def find_2mins(L):
        min1 = min(L)
        L.remove(min1)
        min2 = min(L)  
        return min1, min2 

    def create_LeafQueue(self):
        """ Initalize Nodes: at the beginning all Nodes are Leaf Nodes """

        weight = self.weight_dict()
        ordered_queue = [(k, v) for k, v in sorted(weight.items(), key=lambda item: item[1])]
        for x in ordered_queue:
            x = Node(x[0], x[1])
            self.Leaf_queue.append(x)

    def tree(self):
        self.create_LeafQueue()
        while len(self.Leaf_queue) + len(self.Internal_queue) > 1:
            node1, node2 = TreeBuilder.find_2mins(self.Leaf_queue[0:2] + self.Internal_queue[0:2])
            for node in [node1, node2]:    
                if node in self.Leaf_queue[0:2]:
                    self.Leaf_queue.remove(node)
                else:
                    self.Internal_queue.remove(node)
            new_node = Node(None, node1.wgt + node2.wgt)
            new_node.child1 = node1
            new_node.child2 = node2
            self.Internal_queue.insert(0, new_node)
            