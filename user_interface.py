import queryattempt
import parser

if __name__ == "__main__":

    # making connection to database ONCE
    cred, db = queryattempt.connect_to_database()
    
    print("Welcome to our query interface. Type 'exit' if you wish to do so. Type 'help' to display a help menu with querying.")
    while True:
        user_query = input("> ")
        if user_query.lower() == "exit":
            break
        elif user_query.lower() == "help":
            parser.help_func()
        else:
            parsed_query = parser.parser(user_query)

            if parsed_query == False:
                # if parser returns false show help function and get new user response
                parser.help_func()
                continue
            
            rtn_value = queryattempt.make_query(parsed_query, db)
            
            if len(rtn_value) == 0:
                print('No values found for this query. ')
                continue
            
            # output of successful query 
            for i in range(len(rtn_value)):
                if i + 1 != len(rtn_value):
                    print(f'{rtn_value[i]}, ', end='')
                else:
                    print(f'{rtn_value[i]}')