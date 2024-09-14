

def help():
    print('\nhelp function stuff\n')


def main():
    
    operators = ['==','>','<','and']

    program_running = True

    while program_running:
        query = input('> ')
        if query.lower() == 'help':
            help()
        elif query.lower() == 'exit':
            program_running = False
        else:
            # TODO: parse string
            # TODO: handle any errors
            pass


if __name__ == '__main__':
    main()