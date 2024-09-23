# TODO: REWRITE HELP FUNCTION
def help_func():
    # print('The following you query is incorrect. Here are some tips and examples to help you.')
    # I think we should have help be a keyword instead and just display errors when they query wrong

    help_block = '''

    HELP
    ------
    To exit program, type "exit".
    
    How to query:

    1) Pick one or more from the following keywords:
        - track
        - artist
        - genre
        - released (date song released)
        - subgenre

    2) Select an operator (==, <, >).
        - If you want to perform a compound query (e.g. you want to query against two statements) use "and" in between your statements 
          on the same line

    3) When inputting your query information after your operator (e.g. the song name or the date), please use quotation marks around
       the information if it is longer than 1 word.

    4) Examples:
        - genre == "rap" 
        - subgenre == "gangster rap"
        - genre == "rap" and subgenre == "gangster rap"
        
    
    '''
    
    print(help_block)
    

def parse_query(query):
    # NEW RESTRAINTS 
    # using split and list comprehensions for regex
    operator_pattern = ['==', '>', '<', 'AND']
    keyword_pattern = ["track", "artist", "genre", "released", "subgenre"]
    
    # check if there is an and:
    split_query = query.split('AND')
    query_info = []
    for i in range(len(split_query)):
        index1 = split_query[i].index('*')
        index2 = split_query[i].rindex('*')
        # want to create var so we can create a new string without this inside it 
        string = split_query[i][index1 + 1:index2]
        # append to query info 
        query_info.append(string)
        # deleting that from string 'techincally' kinda (immutable but not rlly)
        split_query[i] = split_query[i].replace('*' + string + '*', ' ')

    operators = []
    keywords = []

    for i in range(len(split_query)):
        split_lst = split_query[i].split(' ')
        for split in split_lst:
            if split in operator_pattern:
                operators.append(split)
            if split in keyword_pattern:
                keywords.append(split)
    
    queries = []
    for i in range(len(keywords)):
        queries.append(keywords[i])
        queries.append(operators[i])
        queries.append(query_info[i])
        if i + 1 != len(keywords):
            queries.append('AND')


    # return value = [[], 'AND', []]

    # print(f'Keywords {keywords}\n')        
    # print(f'Operators {operators}\n')
    # print(f'Query info {query_info}\n')
    print(queries)


