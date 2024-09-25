import queryattempt


def help_func():
    help_block = '''

    HELP
    ------
    To exit program, type "exit".
    
    How to query:

    1) Pick one or more from the following keywords:
        - track
        - artist
        - genre
        - album_name
        - dance_ability
        - subgenre

    2) Select an operator (==, <, >, AND).
        - If you want to perform a compound query (e.g. you want to query against two statements) use "AND" in between your statements 
          on the same line. AND has to be capitalized. 
        - Note that some keywords will no be compatible with certain operators. e.g genre > *5*

    3) When inputting your query information after your operator (e.g. the song name or the date), please use asterisks around
       the information. 

    4) Examples of correct queries:
        - genre == *rap* 
        - subgenre == *gangster rap*
        - genre == *rap* AND subgenre == *gangster rap*
        
    '''
    
    print(help_block)

def parser(query):
    # defining our required operators and keywords
    operator_pattern = ['==', '>', '<', 'AND']
    keyword_pattern = ["track", "artist", "genre", "subgenre", "dance_ability", "album_name"]
    
    # check if there is an and:
    split_query = query.split('AND')
    query_info = []

    try:
        for i in range(len(split_query)):
            # indexing off asterisks
            index1 = split_query[i].index('*')
            index2 = split_query[i].rindex('*')

            # want to create var so we can create a new string without this inside it 
            string = split_query[i][index1 + 1:index2]

            # append to query info 
            query_info.append(string)

            # deleting that from string 'techincally' kinda (immutable but not rlly)
            split_query[i] = split_query[i].replace('*' + string + '*', ' ')

    except ValueError:
        # if there are no asterisks 
        print('No')
        return False

    # loop through rest of query to get opeators, keywords
    operators = []
    keywords = []

    for i in range(len(split_query)):
        split_lst = split_query[i].split(' ')
        for split in split_lst:
            if split in operator_pattern:
                operators.append(split)
            if split in keyword_pattern:
                keywords.append(split)
    
    # formatting return 
    queries = []
    for i in range(len(keywords)):
        queries.append(keywords[i])
        queries.append(operators[i])
        queries.append(query_info[i])
        if i + 1 != len(keywords):
            queries.append('AND')
    
    print(queries)
    return queries
