class Node():
    """ This class defines nodes of the tree, each node contains a character or a string 
    of characters and its weight. Introduces a way to 'compare' nodes."""

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
    """Builds a tree. To build it, we use 2 queues: one Leaf_queue, which contains 
    1-character-nodes, and one Internal_queue for the other nodes.""" 

    def __init__(self, text):
        self.text = text
        self.Leaf_queue = []
        self.Internal_queue = []
        self.Root_Node = None

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
    """ Finds the 2 smallest nodes of a list of nodes"""

        L_copy = L[:]
        min1 = min(L_copy)
        L_copy.remove(min1)
        min2 = min(L_copy)  
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
            new_node = Node(node1.char + node2.char, node1.wgt + node2.wgt)
            new_node.child1 = node1
            new_node.child2 = node2
            self.Internal_queue.insert(0, new_node)
            if len(self.Internal_queue) == 1 and len(self.Leaf_queue) == 0:
                self.Root_Node = self.Internal_queue[0]
                return(self.Root_Node)
                
test_text = "a dead dad ceded a bad babe a beaded abaca bed"
builder = TreeBuilder(test_text)
binary_tree = builder.tree()

class Codec():

    def __init__(self, binary_tree : Node):
        self.binary_tree = binary_tree
    
    def encode(self, text : str):
        code = ""
        for letter in text:
            added_code = ""
            examined_node = self.binary_tree
            while examined_node.char != letter:
                if letter in examined_node.child1.char:
                    added_code += "0"
                    examined_node = examined_node.child1
                else:
                    added_code += "1"
                    examined_node = examined_node.child2
            code += added_code
        return code
            

    def decode(self, code : str):
        text = ""
        i = 0
        while i <= len(code) - 1: 
            examined_node = self.binary_tree
            j = 0
            while len(examined_node.char) != 1:
                if code[i + j] == "0":
                    examined_node = examined_node.child1
                if code[i + j] == "1":
                    examined_node = examined_node.child2
                j += 1
            text += examined_node.char
            i += j
        return text

