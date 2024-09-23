import queryattempt

def parser(query):
    # defining our required operators and keywords
    operator_pattern = ['==', '>', '<', 'AND']
    keyword_pattern = ["track", "artist", "genre", "subgenre", "dance_ability"]
    
    # check if there is an and:
    split_query = query.split('AND')
    query_info = []

    try:
        for i in range(len(split_query)):
            index1 = split_query[i].index('*')
            index2 = split_query[i].rindex('*')
            # want to create var so we can create a new string without this inside it 
            string = split_query[i][index1 + 1:index2]
            # append to query info 
            query_info.append(string)
            # deleting that from string 'techincally' kinda (immutable but not rlly)
            split_query[i] = split_query[i].replace('*' + string + '*', ' ')
    except ValueError:
        print('No')
        return False

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
        
    return queries

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


if __name__ == "__main__":
    # making connection to database one time 
    cred, db = queryattempt.connect_to_database()
    
    print("Welcome to our query interface. Type 'exit' if you wish to do so. Type 'help' to display a help menu with querying.")
    while True:
        user_query = input("> ")
        if user_query.lower() == "exit":
            break
        elif user_query.lower() == "help":
            help_func()
        else:
            parsed_query = parser(user_query)
            if parsed_query == False:
                help_func()
                continue
            # print(parsed_query)
            # try:
            rtn_value = queryattempt.make_query(parsed_query, db)
            # except:
            #     print('Invalid query')
            #     help_func()
            #     continue

            # output of empty return value
            if len(rtn_value) == 0:
                print('No values found for this query. ')
            
            # output of successful query 
            for i in range(len(rtn_value)):
                if i + 1 != len(rtn_value):
                    print(f'{rtn_value[i]}, ', end='')
                else:
                    print(f'{rtn_value[i]}')