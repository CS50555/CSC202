from typing import *
from dataclasses import dataclass
import unittest


# put all of your functions and test cases in this file, yay!
#Data Definition: hashtable is a class with a size (int) object, table (list object), and count (int) object
#Purpose statement: In this class I am creating a HashTable
#Header: this class represents a hashtable, which can create a hash table, count elements in a hash table, tell whether hash table is full and print the hashtable
@dataclass
class HashTable:
    size: int
    table: list
    count: int

    # Data Definition: This method just takes in the hashtable and returns another hashtable
    # Purpose statement: In this method, I am creating a new empty hash table
    # Header: This method creates an empty hash table the size that the user inputs and returns it
    def create_hash(self):
        self.table = [None] * self.size
        return self.table

    # Data Definition: This method just takes in the hashtable and returns an int counts
    # Purpose statement: In this method, I am counting the amount of elements in the hash table
    # Header: This method returns the amount of elements in the hash table
    def counts(self):
        counts = 0
        for i in self.table:
            if i != None:
                counts += 1
        self.count = counts
        return counts

    # Data Definition: This method just takes in the hashtable and returns None
    # Purpose statement: In this method, I am printing the hash table
    # Header: This method prints the hash table and does not return anything
    def show_hash(self):
        print(self.table)
        return None

    # Data Definition: This method just takes in the hashtable and returns True or False
    # Purpose statement: In this method, I am returning true if the table is full and false if it is not
    # Header: This method returns a bool stating whether the table is full or not
    def full(self):
        if None not in self.table:
            return True
        else:
            return False


# Data Definition: This function just takes in the size of the hash table (int) and returns another hashtable
# Purpose statement: In this function, I am creating a new hash table
# Header: This function uses the create hash method to create a new empty hash table the size that the user inputs
def make_hash(size: int) -> HashTable:
    if size > 0:
        newhash = HashTable(size, None, None)
        newhash.create_hash()
        return newhash


# Data Definition: This function just takes in a hashtable and returns an int
# Purpose statement: In this function, I am returning the size of the hash table
# Header: This function returns the size of an inputted hash table
def hash_size(ht: HashTable) -> int:
    return len(ht.table)


# Data Definition: This function just takes in a hashtable and returns an int
# Purpose statement: In this function, I am counting the amount of elements in a hash table and returning it as an int
# Header: This function uses the counts method to count the amount of elements in a hash table and returns it as an int
def hash_count(ht: HashTable) -> int:
    count = ht.counts()
    return count


# Data Definition: This function just takes in a word and returns its hash index value as an integer
# Purpose statement: In this funciton, calculating the hash index of a word with horners method
# Header: This function returns the hash value of a word
def quadratic_hash(word):
    n = len(word)
    result = 0
    for i in range(n):
        result += ord(word[i]) * (31 ** (n - 1 - i))
    return result




# Data Definition: This function just takes in a hashtable and a word (string) and returns a bool
# Purpose statement: In this function, I am checking whether the word ("key") is in the hashtable and returning a bool to tell whether it is or isnt
# Header: This function returns true if the word is in the hashtable and false if not
def has_key(ht: HashTable, word: str) -> bool:
    index = quadratic_hash(word) % ht.size
    start_index = index
    step = 0
    while ht.table[index] is not None:
        if ht.table[index][0] == word:
            return True
        step += 1
        index = (start_index + step ** 2) % ht.size
        if index == start_index:
            break
    return False

# Data Definition: This function just takes in a hashtable returns a list of ints representing page numbers
# Purpose statement: In this method, I am returning the page numbers in a list of a word that is in the hash table
# Header: This function returns the page numbers of a looked up word ("key")
def hash_keys(ht: HashTable) -> List[str]:
    list_keys = []
    for i in ht.table:
        if i != None:
            list_keys.append(i[0])
    return list_keys

# Data Definition: This function just takes in a file and returns a list
# Purpose statement: This function reads all of the stop_words from the stopwords file and returns a list of them
# Header: This function returns all of the stop words from a file into a list for the concordance funciton
def read_stop_words(file_path):
    try:
        new_list = []
        with open(file_path, 'r') as file:
            for line in file:
                new_list.append(line.removesuffix('\n'))
            return new_list
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Data Definition: This function just takes in a file and returns a list
# Purpose statement: This function reads all of the lines from the text file and returns a string of all of the text
# Header: This function concatonates a list of words in the file into a string to be cleaned
def read_test(file_path):
    try:
        listoflines = []
        with open(file_path, 'r') as file:
            for line in file:
                listoflines.append(line)
        new_string = ''.join(listoflines)
        return new_string
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Data Definition: This function just takes in a string and returns a list
# Purpose statement: This function takes the apostrophes out of string and lowercases/takes out any punctuation
# Header: This function cleans the string and turns it into a list if alpha is true or if a newline
def clean_text(text: str):
    if "'" in text:
        text = text.replace("'", "")
    new_text = text.replace('.', ' ').replace('?', ' ').replace('!', ' ').replace(',', ' ').lower().replace("\n", " \n ").replace('/', ' ')
    listofwords = new_text.split(' ')
    new_list = [x for x in listofwords if x.isalpha() or x == '\n']
    return new_list

# Data Definition: This function just takes in two lists (stop words and text) and returns a hashtable
# Purpose statement: This function makes a hash table for both the stop_words and the text words
#it then checks the text hash against the stop_words hash to not include the stop words into the hash
# and then it adds a line number for every newline break character
#it then creates a new hash table with the values
# Header: This function essentially makes a hashtable from the words in the text file and excludes words from the stop_words file
def make_concordance(stop_words: List[str], text: List[str]) -> HashTable:
    stop_words_hash = make_hash(128)
    text_hash = make_hash(128)
    for i in range(len(stop_words) - 1):
        add(stop_words_hash, stop_words[i], i)
    line_number = 1
    for word in text:
        if word != '\n' and not has_key(stop_words_hash, word):
            add(text_hash, word, line_number)
        elif word == '\n':
            line_number += 1
    temp_hash = make_hash(text_hash.size)
    finalhash = rehash(text_hash, temp_hash)
    return finalhash

# Data Definition: This function just takes in a hash table and a string of the output file and returns None
# Purpose statement: This function writes the hash table values to the concordance_output file
# Header: This function writes the hash table values to the concordance_output file
def generate_concordance_file(ht: HashTable, output_file_path: str) -> None:
    with open(output_file_path, 'w') as output_file:
        for word in sorted(hash_keys(ht)):
            line_numbers = ' '.join(map(str, lookup(ht, word)))  #make list of page nums strings and join them into one string
            output_file.write(f"{word}: {line_numbers}\n")


# Data Definition: This function just takes in a hash table and returns a hash table
# Purpose statement: This function doubles the size of the hash table when it is full
# Header: This function doubles the size of the hash table when it is full
def grow_hash(ht: HashTable) -> HashTable:
    new_htsize = ht.size * 2
    newht = make_hash(new_htsize)
    newhash = rehash(ht, newht)
    return newhash

# Data Definition: This function just takes in two hash tables hash table and returns a hash table
# Purpose statement: This function inserts words into the hashtable in the correct place
# Header: This function inserts words into the hashtable in the correct place
def rehash(ht: HashTable, temp_ht: HashTable) -> HashTable:
    for i in ht.table:
        if i is not None:
            add(temp_ht, i[0], i[1]) #fix list insertion
    ht.table = temp_ht.table
    ht.size = temp_ht.size
    return ht

# Data Definition: This function just takes in a hash table, a word, and a list of line numbers and returns None
# Purpose statement: This function adds the word and line numbers to the hashtable
# Header: This function adds the word and line numbers to the hashtable
#take in hash table word and line
#if hash is full, grow and rehash
#else
#calculate index
#quadratically probe and add when ht[index] is None
def add(ht: HashTable, word: str, line: int) -> None:
    index = quadratic_hash(word) % ht.size                        #calculate hash index
    if has_key(ht, word) == True and ht.table[index][0] == word:  # if word alread in hash, add line to list the line numbers
        ht.table[index][1].append(line)
        return None
    if type(line) is int and has_key(ht, word) is False:  #if it is an int and the word is not already in hashtable, make it into a list
        line_list = [line]
    elif type(line) is list and has_key(ht, word) is True:
        line_list = line                                   #if in hashtable alread and already is a list, keep line as an int
    else:
        line_list = line
    if ht.full():  #if full, grow hash and rehash table
        grow_hash(ht)
    if ht.table[index] is None:
        ht.table[index] = word, line_list
    else:
        step = 1
        next_index = (index + step ** 2) % ht.size
        while next_index != index and ht.table[next_index] is not None:
            if has_key(ht, word) == True and ht.table[next_index][0] == word: #if word in hash at next value, add to list and break out
                ht.table[next_index][1].append(line_list)
                return None
            step += 1
            next_index = (index + step ** 2) % ht.size
        ht.table[next_index] = word, line_list

# Data Definition: This function just takes in a hash table and a word and returns a list of ints
# Purpose statement: This function uses the key to return the page numbers associated with that key
# Header: This function uses the key to return the page numbers associated with that key
def lookup(ht: HashTable, word: str) -> List[int]:
    index = quadratic_hash(word) % ht.size
    start_index = index
    step = 0
    while ht.table[index] is not None:
        if ht.table[index][0] == word:
            return ht.table[index][1]
        step += 1
        index = (start_index + step ** 2) % ht.size


#this code allows the user to input the name of the input text file which will then output to concordance_output.txt
#INSTRUCTIONS ON HOW TO CALL PROGRAM
#1. input name of input file when prompted in terminal (without adding '.txt' (the main input file in this folder is 'text.txt')
#2. concordance will be outputted to concordance_output.txt
print("INPUT TEXTFILE HERE (DON'T INCLUDE '.txt'): ")
print("For test cases type 'text' when prompted.")
#userinput = input() + ".txt"  #input text file    TO USE INPUT FUNCTION UNCOMMENT THIS LINE, DELETE LINE AFTER, AND USE AS INSTRUCTED (HAD TO DO THIS FOR AUTOGRADER TO WORK)
userinput = "text.txt"
stringoftext = read_test(userinput) #processing text file
cleaned_text = clean_text(stringoftext) #cleaning text file
stop_words = read_stop_words('stop_words.txt') #get stop words
concordance = make_concordance(stop_words, cleaned_text) #input text and stop words into concordance file
generate_concordance_file(concordance, 'concordance_output.txt') #output concordance to concordance_output.txt


# put all test cases in the "Tests" class.
class Tests(unittest.TestCase):

#positive test case
    def test_make_hash(self):
        result = make_hash(5)
        expected = HashTable(size=5, table=[None, None, None, None, None], count=None)
        self.assertEqual(result, expected)

#negative test case
    def test_make_hash1(self):
        result = make_hash(-5)
        expected = None
        self.assertEqual(result, expected)

#positive test case
    def test_hash_size(self):
        result = make_hash(12)
        expected = HashTable(size=12, table=12*[None], count=None)
        self.assertEqual(result, expected)

#positive test case
    def test_hash_size1(self):
        result = make_hash(4)
        expected = HashTable(size=4, table=4*[None], count=None)
        self.assertEqual(result, expected)

#negative test case
    def test_hash_size2(self):
        result = make_hash(-4)
        expected = None
        self.assertEqual(result, expected)

#positive test case
    def test_create_hash_method(self):
        obj = HashTable(4, [], 0)
        result = obj.create_hash()
        expected = 4*[None]
        self.assertEqual(result, expected)


#positive test case
    def test_create_hash_method1(self):
        obj = HashTable(5, [], 0)
        result = obj.create_hash()
        expected = 5*[None]
        self.assertEqual(result, expected)

#positive test case
    def test_hash_count(self):
        obj = HashTable(5, [None, 4, None, 2, None], 0)
        result = hash_count(obj)
        expected = 2
        self.assertEqual(result, expected)

# positive test case
    def test_hash_count1(self):
        obj = HashTable(6, [None, 4, None, "hello", None, 9.8], 0)
        result = hash_count(obj)
        expected = 3
        self.assertEqual(result, expected)

#positive test case
    def test_count(self):
        obj = HashTable(6, [None, 4, None, "hello", None, 9.8], 0)
        result = obj.counts()
        expected = 3
        self.assertEqual(result, expected)

#positive test case
    def test_full1(self):
        obj = HashTable(6, [None, 4, None, "hello", None, 9.8], 0)
        result = obj.full()
        expected = False
        self.assertEqual(result, expected)

#positive test case
    def test_full(self):
        obj = HashTable(6, [None, 4, None, "hello", None, 9.8], 0)
        result = obj.full()
        expected = False
        self.assertEqual(result, expected)

#positive test case
    def test_full2(self):
        obj = HashTable(6, [3, 4, 3, "hello", 3, 9.8], 0)
        result = obj.full()
        expected = True
        self.assertEqual(result, expected)

#positive test case
    def test_count1(self):
        obj = HashTable(6, [None, 4, None, "hello", 1, 9.8], 0)
        result = obj.counts()
        expected = 4
        self.assertEqual(result, expected)

#positive test case
    def test_hash_idx(self):
        obj = "a"
        result = quadratic_hash(obj)
        expected = 97
        self.assertEqual(result, expected)

#positive test case
    def test_hash_idx1(self):
        obj = "cat"
        result = quadratic_hash(obj)
        expected = 98262
        self.assertEqual(result, expected)

# positive test case
    def test_has_key(self):
        obj = HashTable(6, [None, "a", None, "b", None, "hello"], 3)
        result = has_key(obj, "a")
        expected = True
        self.assertEqual(result, expected)

# positive test case
    def test_has_key1(self):
        obj = HashTable(6, [None, ("a", 4), None, ("b", 8), ("hello", 3), ("c", 10)], 3)
        result = has_key(obj, "hello")
        expected = True
        self.assertEqual(result, expected)

# positive test case
    def test_has_key2(self):
        obj = HashTable(6, [None, ("a", 4), None, ("b", 8), ("hello", 3), ("c", 10)], 3)
        result = has_key(obj, "no")
        expected = False
        self.assertEqual(result, expected)

# positive test case
    def test_hash_keys(self):
        obj = HashTable(6, [None, ("a", [4]), None, ("b", [8]), ("hello", [3]), ("c", [10])], 3)
        result = hash_keys(obj)
        expected = ['a', 'b', 'hello', 'c']
        self.assertEqual(result, expected)

# positive test case
    def test_hash_keys1(self):
        obj = HashTable(3, [("t", [8]), ("no", [3]), ("c", [10])], 3)
        result = hash_keys(obj)
        expected = ['t', 'no', 'c']
        self.assertEqual(result, expected)

# positive test case
    def test_read_stop_file(self):
        obj = "stop_words.txt"
        result = read_stop_words(obj)
        expected = ['a', 'about', 'be', 'by', 'can', 'do', 'i', 'in', 'is', 'it', 'of', 'on', 'the', 'this', 'to', 'was']
        self.assertEqual(result, expected)

# positive test case
    def test_read_test_file(self):
        obj = "test.txt"
        result = read_test(obj)
        expected = "This is a sample data ((text)) file, to be \nprocessed by your word-concordance program!!!\n\nA REAL data file is MUCH bigger. Gr8!"
        self.assertEqual(result, expected)

# positive test case
    def test_clean_test(self):
        obj = "Hello 2gl the car's whe3ls are not !!\n worn. out, but they'll \n ?work."
        result = clean_text(obj)
        expected = ['hello', 'the', 'cars', 'are', 'not', '\n', 'worn', 'out', 'but', 'theyll', '\n', 'work']
        self.assertEqual(result, expected)

# negative test case
    def test_clean_test2(self):
        obj = "!!' 929' ?.../"
        result = clean_text(obj)
        expected = []
        self.assertEqual(result, expected)

# positive test case
    def test_grow_hash(self):
        obj = HashTable(6, [None, ("a", [4]), None, ("b", [8]), ("hello", [3]), ("c", [10])], 3)
        result = grow_hash(obj)
        expected = HashTable(size=12, table=[None, ('a', [4]), ('b', [8]), ('c', [10]), None, None, None, None, None, None, ('hello', [3]), None], count=3)
        self.assertEqual(result, expected)

# positive test case
    def test_grow_hash1(self):
        obj = HashTable(3, [("c", [8]), ("no", [3]), ("was", [10])], 3)
        result = grow_hash(obj)
        expected = HashTable(size=6, table=[None, ("was", [10]), None, ('c', [8]), None, ("no", [3])], count=3)
        self.assertEqual(result, expected)

# positive test case
    def test_rehash(self):
        obj = HashTable(3, [("c", [8]), ("no", [3]), ("was", [10])], 3)
        temp = HashTable(3, 3*[None], 0)
        result = rehash(obj, temp)
        expected = HashTable(3, [("c", [8]), ("was", [10]), ("no", [3])], 3)
        self.assertEqual(result, expected)



# positive test case
    def test_rehash1(self):
        obj = HashTable(6, [None, ("a", [4]), None, ("b", [8]), ("hello", [3]), ("c", [10])], 3)
        temp = HashTable(6, 6*[None], 0)
        result = rehash(obj, temp)
        expected = HashTable(6, [None, ("a", [4]), ("b", [8]), ("c", [10]), ("hello", [3]), None], 3)
        self.assertEqual(result, expected)

# positive test case
    def test_add(self):
        obj = HashTable(6, [None, ("a", [4]), None, ("b", [8]), ("hello", [3]), ("c", [10])], 3)
        word = "star"
        line = 9
        add(obj, word, line)
        intable = has_key(obj, word)
        expected = True
        self.assertEqual(intable, expected)

# positive test case
    def test_lookup(self):
        obj = HashTable(6, [None, ("a", [4]), None, ("b", [8]), ("hello", [3]), ("c", [10])], 3)
        word = "a"
        result = lookup(obj, word)
        expected = [4]
        self.assertEqual(result, expected)

# negative test case
    def test_lookup1(self):
        obj = HashTable(6, [None, ("a", [4]), None, ("b", [8]), ("hello", [3]), ("c", [10])], 3)
        word = "all"
        result = lookup(obj, word)
        expected = None
        self.assertEqual(result, expected)

#concordance function tested with sample test file and outputted the correct output file