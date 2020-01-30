#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Realizes Huffman coding """

class Node():
    """ This class defines nodes of the tree, each node contains a character or a string 
    of characters and its weight. Also introduces a way to 'compare' nodes."""

    def __init__(self, char : str, wgt : int):
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
    """Builds a tree. To build it, we use a Node_queue""" 

    def __init__(self, text : str):
        self.text = text
        self.Node_queue = []
        self.Root_Node = None

    def weight_dict(self):  
        """ Creates a dictionary with the weight of each character """

        weight = {}
        for character in self.text:
            if not character in weight:
                 weight[character] = 0
            weight[character] += 1
        return weight

    @staticmethod
    def find_2mins(L : list):
        """ Finds the 2 smallest nodes of a list of nodes"""

        L_copy = L[:]
        min1 = min(L_copy)
        L_copy.remove(min1)
        min2 = min(L_copy)  
        return min1, min2 

    def create_Node_Queue(self):
        """ Initalizes Node_Queue thanks to the dictionary created by TreeBuilder.weight_dict """

        weight = self.weight_dict()
        # We stock Nodes by weight-ascending order
        ordered_queue = [(k, v) for k, v in sorted(weight.items(), key=lambda item: item[1])]
        for x in ordered_queue:
            x = Node(x[0], x[1])
            self.Node_queue.append(x)

    def tree(self):
        """ We build the tree by creating a new node from the two-least-weighted nodes of the
        Node_queue. We remove these two 'smallest' nodes and repeat the process """

        self.create_Node_Queue()
        while len(self.Node_queue) > 1:
            node1, node2 = TreeBuilder.find_2mins(self.Node_queue)
            for node in [node1, node2]:  
                self.Node_queue.remove(node)  
            new_node = Node(node1.char + node2.char, node1.wgt + node2.wgt)
            new_node.child1 = node1
            new_node.child2 = node2
            self.Node_queue.insert(0, new_node)
            if len(self.Node_queue) == 1:
                self.Root_Node = self.Node_queue[0]
                return(self.Root_Node)

class Codec():
    """ Contains encode and decode methods, which depend on the binary_tree provided 
    by the user """

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

