from typing import *
from dataclasses import dataclass
import unittest

# put all of your functions and test cases in this file, yay!


#This class HNode Represents each Leaf of node in a tree (Leaf is a Node without children)
#Each node has a character and a occurrence value (hvalue) as well as a left and right node
@dataclass
class HNode:
    character: str
    hvalue: int
    left_leaf: 'HNode' = None
    right_leaf: 'HNode' = None


#This class represents a leaf, but I just used the HNode class to represent leaves too
@dataclass
class HLeaf:
    character: str
    hvalue: int


#This is a linked list of Trees (Nodes)
#It also has a Node class with the value of the node as well as the next node
@dataclass
class Node:
    value: HNode
    next: 'Node' = None


#this is the class that represents the linked list itself
@dataclass
class HTList:
    head: 'Node' = None

    #this function appends a leaf to the end of a linked list
    def append_leaf(self, Hnode):  #append new node with leaf  GOOD
        new_node = Node(Hnode)   #create a new_node in doubly linked list with a leaf that contains occurrence count
        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node


    #need a function to calculate the length of the linked list
    def lenlist(self):
        count = 0
        current_node = self.head
        while current_node is not None:
            count += 1
            current_node = current_node.next
        return count

    def insert_in_position(self, Hnode):
        new_tree = Node(Hnode)
        if self.head is None:
            self.head = new_tree
        else:
            current_tree = self.head
            occurrence_val = new_tree.value.hvalue  # Access the 'hvalue' attribute of HNode
            while current_tree is not None:
                if current_tree.value.hvalue < occurrence_val <= current_tree.next.value.hvalue:
                    new_tree.next = current_tree.next
                    current_tree.next = new_tree
                current_tree = current_tree.next


    #this function should return and delete the smallest number
    #if smaller num make it the head
    #return and delete head
    def delete_smallest(self):  #not done
        htlist = HTList()
        smallestNode = self.head.value
        if self.head is None:
            return None
        else:
            current = self.head   #current is current node
            smallest = self.head.value.hvalue  #smallest is the value of the node
            while current.next is not None:  #this part finds the smallest value
                if current.next.value.hvalue < smallest:
                    smallest = current.next.value.hvalue
                    smallestNode = current.next.value
                current = current.next

            current = self.head
            while current.next is not None:    #this part deletes the node of hte smallest value
                if current.value.hvalue == smallest:
                    self.head = current.next
                    break
                elif current.next.value.hvalue == smallest:
                    current.next = current.next.next
                    break
                current = current.next
            return smallestNode


    #this adds the combined node to the beginning of the list
    def add_beginning(self, node):
        new_node = Node(node)
        new_node.next = self.head
        self.head = new_node

    #this function deletes the first two nodes in the linked list to be replaced with collapsed node
    def delete_first_two(self):
        for i in range(0,2):
            if self.head is not None:
                self.head = self.head.next



    #iterate thru list
    #grab smallest value
    #remove smallest
    #grab smallest
    #repeat
#this function sorts the linked list
    def sort(self):
        new_list = HTList()
        length = htlist.lenlist()
        for i in range(length):
            smallest = htlist.delete_smallest()
            new_list.append_leaf(smallest)
        return new_list


    #this function combines the two nodes into one in order to make the huffman tree
    def combinenodes2(self):
        current_node = self.head
        occurrencesum = 0
        for i in range(0,2):
            occurrencesum += current_node.value.hvalue
            if i == 1:
                larger_node = current_node.value
            else:
                smaller_node = current_node.value
            current_node = current_node.next

        return HNode(larger_node.character, occurrencesum, smaller_node, larger_node)


    #this function prints out the huffman tree
    def showtree(self):
        current_node = self.head
        while current_node is not None:
            print(f"{current_node.value} -> ")
            current_node = current_node.next
        return None

#this funcion utilizes the numpy array to keep track of the frequencies of the letters in a given string (File)
#it does this by adding everytime a certain letter (mapped to ASCII code) is used in the string
#then it returns the array
def cnt_freq(str):
    counts = [0]*256 #initialize all elements in array to zero
    for character in str:
        char_code = ord(character)  #input ASCII values of character into array
        if 0 <= char_code <= 255:  #check if ASCII Value is in range
            counts[char_code] += 1  #accumulate to charcode value in array

    return counts

#this funciton compares whether the character ord is larger in tree a than tree b
def tree_lt(a,b):
    return cnt_freq(a.character) < cnt_freq(b.character)




#the baselift function accepts an array of character counts and returns an HList containing
#the 256 HTLeafs -> one for each ASCII code

def base_tree_list(charcnts):  #takes in charcounts array
    htlist = HTList()   #creates a doubly linked list
    for i in range(0, 255):   #MAKE 255 AGAIN iterates through 0-255 and appends each value in character counts into the doubly linked list
        char = chr(i)
        htlist.append_leaf(HNode(char, charcnts[i], None, None))
    return htlist


#tree_list_insert takes htlistlist of HTtrees that is sorted and another tree and inserts it into list at correct place
def tree_list_insert(htlist, tree):
    occurence_count_tree = tree
    htlist.insert_in_position(occurence_count_tree)
    return htlist


#this function sorts the tree's nodes fron least to greatest by creating a new list
def initial_tree_sort(htlist):
    sorted_list = htlist.sort()
    print(sorted_list)
    return sorted_list

#this function mergest two trees into one huffman tree
def coalesce_once(htlist): #need to test htlist length method
    if htlist.lenlist() < 2:
        print("list too short: must be at least two trees")
        return None
    else:   #get first two nodes, add occurrence values, make str the second nodes value
        combined_node = htlist.combinenodes2()
        htlist.delete_first_two()
        htlist.add_beginning(combined_node)
    return htlist

#this function keeps running the coalesce once function until it is left with one huffman tree
def coalesce_all(htlist): #need to test htlist length method
    while htlist.lenlist() > 1:
        htlist = coalesce_once(htlist)  # Call coalesce_once repeatedly until one tree remains
    return htlist.head.value




#this function recursively travels through the left and right nodes of the tree
#it adds a 0 every time it travels left and a 1 every time it travels right
#it places the code at the ith element in the list represented by the ASCII Value
def build_encoder_array(tree, path, encoder_array):
    if tree is not None:
        if tree.character is not None:
            char_code = ord(tree.character)  #create idx num with character ASCII Value
            while len(encoder_array) <= char_code:
                encoder_array.append('')  # Extend the list if needed
            build_encoder_array(tree.left_leaf, path + '0', encoder_array)  # recursively go down left path and add 0s
            build_encoder_array(tree.right_leaf, path + '1', encoder_array)  # recursively go down righ path and add 1s
            encoder_array[char_code] = path   #make a pack (represented by a string) that replaces char code element with 0s and 1s

    return encoder_array



#this function encodes the huffman string (1s and 0s) by connecting the 1s and 0s and creates the string
#by appending the codes from the huffman tree
def encode_string_one(input_string, encoder_array):
    encoded_string = ''    #start with empty string to add to
    for char in input_string:    #iterate through input_string and for each char, get ASCII Value and add from encoder array w ASCII Value
        char_code = ord(char)    #to append to string
        encoded_string += encoder_array[char_code]
    return encoded_string

#This function changes the bits from the encode_string_one to characters
#it makes the bits into bytes (8 bit wordlength) then it
def bits_to_chars(bits):
    # Pad the input string with zeros to make its length a multiple of 8
    pad_length = 8 - (len(bits) % 8)    #figure out how many zeros are needed to pad bit
    bits += '0' * pad_length            #this adds 0s to the value to pad it

    char_string = ''                    #make an empty string to add to
    for i in range(0, len(bits), 8):    #iterate through the bits
        # Take each 8-character substring, convert it to an integer, and then use chr to produce a character
        char_code = int(bits[i:i + 8], 2)   #slices string and places 8-bit value at ith index in base 2 (binary)
        char_string += chr(char_code)      #add characters for character code to char_string

    return char_string


htlist = HTList()
htlist.append_leaf(HNode('a', 2, None, None))
htlist.append_leaf(HNode('b', 5, None, None))
htlist.append_leaf(HNode('c', 3, None, None))
htlist.append_leaf(HNode('s', 1, None, None))




def huffman_code_file(source_file, target_file):
    # Read content from the source file
    with open(source_file, 'r') as file:
        content = file.read()
    # Count character frequencies
    words = cnt_freq(content)
    # Create a list of leaves and sort it
    leaves = base_tree_list(words)
    sorted_leaves = initial_tree_sort(leaves)
    #  Build the Huffman tree
    huffman_tree = coalesce_all(sorted_leaves)
    # Build the encoder array
    encoder_array = [''] * 250
    encoder_array2 = build_encoder_array(huffman_tree, '', encoder_array)
    # Encode the content
    encoded_string = encode_string_one(content, encoder_array2)
    #  Convert encoded bits to characters
    chars = bits_to_chars(encoded_string)
    # Write the encoded content to the target file
    with open(target_file, 'w') as file:
        file.write(chars)

    return content



# put all test cases in the "Tests" class.
class Tests(unittest.TestCase):
    # Positive test case to append a leaf in the input function
    def test_append_leaf(self):
        htlist = HTList()
        node1 = (HNode('a', 3, None, None))
        node2 = (HNode('a', 3, None, None))
        htlist.append_leaf(node1)
        htlist.append_leaf(node2)
        self.assertEqual(htlist.head.value, node1)  # Check the first appended node
        self.assertEqual(htlist.head.next.value, node2)  # Check the second appended node
        self.assertIsNone(htlist.head.next.next)  # Check that there are no more nodes

        # Negative test case to append a leaf in the input function

    def test_append_leaf1(self):
        htlist = HTList()
        node1 = (HNode('a', 3, None, None))
        node2 = (HNode('a', 3, None, None))
        htlist.append_leaf(node1)
        htlist.append_leaf(node2)
        self.assertEqual(htlist.head.value, node1)  # Check the first appended node
        self.assertIsNotNone(htlist.head.next)  # Check that there are no more nodes

        # Positive test case to append a leaf in the input function

    def test_cnt(self):
        result = cnt_freq("a")
        expected = [0] * 97 + [1] + [0] * 158
        self.assertEqual(result, expected)

    # negative test case for cntfreq function
    def test_tree_lt1(self):
        node_a = HNode('a', 3, None, None)
        node_b = HNode('b', 7, None, None)
        result = tree_lt(node_a, node_b)
        expected = False
        self.assertEqual(result, expected)

    # negative test case for tree_lt function
    def test_tree_lt2(self):
        node_a = HNode('hello', 3, None, None)
        node_b = HNode('goodbye', 7, None, None)
        result = tree_lt(node_a, node_b)
        expected = True
        self.assertEqual(result, expected)

    # positive test case for tree_list_insert_sorted_list
    def test_tree_list_insert_sorted_list1(self):
        htlist = HTList()
        htlist.append_leaf(HNode('B', 0))
        htlist.append_leaf(HNode('C', 30))
        tree_to_insert = HNode('A', 10)
        result = tree_list_insert(htlist, tree_to_insert)
        self.assertIsNotNone(result.head, "Expected a non-empty HTList")
        self.assertEqual(result.head.value.character, 'B', "Expected character 'B' after 'A'")


    def test_initial_tree_sort_sorted_list2(self):
        htlist = HTList()
        sorted_list = initial_tree_sort(htlist)
        self.assertIsNotNone(sorted_list.head, "Expected a non-empty HTList")

    def test_coalesce_once_multiple_nodes_list1(self):
        htlist = HTList()
        htlist.append_leaf(HNode('A', 15))
        htlist.append_leaf(HNode('B', 20))
        result = coalesce_once(htlist)
        self.assertIsNotNone(result, "Expected a non-empty HTList")
        self.assertEqual(result.head.value.character, 'B', "Expected character 'AB' at the beginning")
        self.assertEqual(result.head.value.hvalue, 35, "Expected combined character count of 30")

    def test_coalesce_once_multiple_nodes_list(self):
        htlist = HTList()
        htlist.append_leaf(HNode('c', 10))
        htlist.append_leaf(HNode('d', 20))
        result = coalesce_once(htlist)
        self.assertIsNotNone(result, "Expected a non-empty HTList")
        self.assertEqual(result.head.value.character, 'd', "Expected character 'AB' at the beginning")
        self.assertEqual(result.head.value.hvalue, 30, "Expected combined character count of 30")

    def test_coalesce_all_multiple_nodes_list1(self):
        htlist = HTList()
        htlist.append_leaf(HNode('A', 10))
        htlist.append_leaf(HNode('B', 20))
        htlist.append_leaf(HNode('C', 30))
        result = coalesce_all(htlist)
        self.assertIsNotNone(result, "Expected a non-empty HTNode")
        self.assertEqual(result.character, 'C', "Expected combined character 'ABC'")
        self.assertEqual(result.hvalue, 60, "Expected combined character count of 60")

    def test_coalesce_all_multiple_nodes_list2(self):
        htlist = HTList()
        htlist.append_leaf(HNode('y', 10))
        htlist.append_leaf(HNode('f', 25))
        htlist.append_leaf(HNode('X', 0))
        result = coalesce_all(htlist)
        self.assertIsNotNone(result, "Expected a non-empty HTNode")
        self.assertEqual(result.character, 'X', "Expected combined character 'ABC'")
        self.assertEqual(result.hvalue, 35, "Expected combined character count of 60")

    # Positive test for encoder array single node tree
    def test_build_encoder_array_single_node_tree(self):
        tree = HNode('A', 10)
        encoder_array = [''] * 256
        build_encoder_array(tree, '', encoder_array)
        expected_encoder_array = [''] * 256
        expected_encoder_array[ord('A')] = ''
        self.assertEqual(encoder_array, expected_encoder_array, "Expected encoder_array with 'A' path")

    def test_build_encoder_array_multiple_nodes_tree2(self):
        tree = HNode(None, 0, HNode('A', 10), HNode('B', 20))
        encoder_array = [''] * 256
        build_encoder_array(tree, '', encoder_array)
        expected_encoder_array = [''] * 256
        expected_encoder_array[ord('A')] = '0'
        expected_encoder_array[ord('B')] = '1'
        self.assertNotEqual(encoder_array, expected_encoder_array, "Expected encoder_array with 'A' and 'B' paths")

    def test_encode_string_single_character_input(self):
        input_string = 'A'
        encoder_array = [''] * 256
        encoder_array[ord('A')] = '01'
        result = encode_string_one(input_string, encoder_array)
        self.assertEqual(result, '01', "Expected encoded string '01'")

    # positive test case for encoding string
    def test_encode_string_multiple_characters_input1(self):
        input_string = 'AB'
        encoder_array = [''] * 256
        encoder_array[ord('A')] = '0'  # Mock encoder_array
        encoder_array[ord('B')] = '1'  # Mock encoder_array
        result = encode_string_one(input_string, encoder_array)
        self.assertEqual(result, '01', "Expected encoded string '01'")

    def test_bits_to_chars_empty_bits(self):
        bits = ''
        result = bits_to_chars(bits)
        self.assertEqual(result, '\x00', "Expected an empty character string")

    def test_bits_to_chars_single_byte(self):
        bits = '01001000'  # Binary for character 'H'
        result = bits_to_chars(bits)
        self.assertEqual(result, 'H\x00', "Expected character 'H\x00'")

    def test_bits_to_chars_multiple_bytes(self):
        bits = '0100100001101001'  # Binary for 'Hello'
        result = bits_to_chars(bits)
        self.assertEqual(result, 'Hi\x00', "Expected character 'Hi\x00'")

    def test_bits_to_chars_padding(self):
        bits = '01001000'  # Binary for 'H', with 2 zeros padding
        result = bits_to_chars(bits)
        self.assertEqual(result, 'H\x00', "Expected character 'H\x00'")

    def test_empty_tree(self):
        # Test with an empty tree, which should return the original empty encoder_array
        tree = None
        encoder_array = build_encoder_array(tree, '', [''] * 256)
        self.assertEqual(encoder_array, [''] * 256)

