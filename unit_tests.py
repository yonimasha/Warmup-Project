# unit tests for parser.py

# TODO: import files
# from parse import *

# TODO: alter below test cases to fit function names if needed

# string parsing test cases
def test1():
    
    given_query = 'genre == rap'
    parsed_string = get_query(given_query)

    if parsed_string != ['genre', '==', 'rap']:
        print("FAILED: TEST 1")
    else:
        print("PASSED: TEST 1")


def test2():
    pass

def test3():
    pass

def test4():
    pass

def test5():
    pass


# TODO: other test cases 