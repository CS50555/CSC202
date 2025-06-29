import unittest
import math
from main import HLeaf, tree_lt, base_tree_list, tree_list_insert, initial_tree_sort, coalesce_once, coalesce_all

# please note: these are not real tests! They don't include
# expected results, and they don't actually test that the
# given functions and methods *work*, they just test to make
# sure that the given methods and functions actually exist,
# and run when called with the right # and kind of arguments.

# your test cases must be better than these! Each of your tests
# should include an assertion containing an expected result.

# Also: you can edit this file, but it's probably not a good idea;
# deleting these tests, for instance, would result in "all tests
# passed" from GitHub... but then your code would fail terribly
# against the post-handin test cases. So just don't edit this file.

class MyTests(unittest.TestCase):

    def test_tree_lt_existence(self):
        tree_lt(HLeaf('a',0),HLeaf('a',0))
        base_tree_list([0 for i in range(256)])
        tree_list_insert([])
        initial_tree_sort([])
        coalesce_once([HLeaf('a',0),HLeaf('a',0)])
        coalesce_all([HLeaf('a',0)])


if (__name__ == '__main__'):
    unittest.main()