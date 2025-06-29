import unittest
from main import make_hash, hash_size, hash_count, has_key, lookup, add, hash_keys, make_concordance

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

    def test_function_existence(self):
        table = make_hash(234)
        hash_size(table)
        hash_count(table)
        has_key(table,'abc')
        lookup(table,'abc')
        add(table,'abc',22)
        hash_keys(table)
        make_concordance(['abc','def'],['line 1','line 2'])


if (__name__ == '__main__'):
    unittest.main()