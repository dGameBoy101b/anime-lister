from os import path
from file_list import FileList

def main():
    PROMPT = '>>> '
    CLOSE_COM = 'close'
    HELP_COM = 'help'
    ADD_COM = 'add'
    VIEW_COM = 'view'
    DELETE_COM = 'remove'
    COM_SEP = ' '
    LIST_FILENAME = 'my_anime_list.csv'
    COM_ERROR = 'Command not recognised!'

    aid()
    while True:
        com = input(PROMPT)
        if com == CLOSE_COM:
            close()
        elif com == HELP_COM:
            aid()
        elif com.partition(COM_SEP)[0] == ADD_COM:
            add(LIST_FILENAME, com.partition(COM_SEP)[2])
        elif com.partition(COM_SEP)[0] == VIEW_COM:
            view(LIST_FILENAME, com.partition(COM_SEP)[2])
        elif com.partition(COM_SEP)[0] == DELETE_COM:
            delete(LIST_FILENAME, com.partition(COM_SEP)[2])
        else:
            print(COM_ERROR)

def close():
    raise SystemExit

def aid():
    HELP_TEXT = (
        'close: close the program',
        'help: display this help text',
        'view *max_items*: display titles on your anime list',
        '\t*max_items*: the maximum number of titles to display (leave blank for all titles)',
        'add *anime_title*: add an anime title to your list',
        '\t*anime_title*: the anime title you wish to add',
        'remove *anime_title*: remove an anime title from your list',
        '\t*anime_title*: the anime title you wish to remove',
        )
    
    for item in HELP_TEXT:
        print(item)

def add(filename: str, title: str):
    EMPTY_ERROR = '*anime_title* cannot be empty!'
    EXIST_ERROR = '"{0}" is already on your anime list!'
    ADD_SUCCESS = 'Added "{0}" to your anime list.'

    if title == '':
        print(EMPTY_ERROR)
        return
    file = FileList(filename)
    if file.find(title) != -1:
        print(EXIST_ERROR.format(title))
    else:
        file.append(title)
        print(ADD_SUCCESS.format(title))

def view(filename: str, num: int = None):
    INT_ERROR = '*max_items* must be a number!'
    NUM_ERROR = '*max_items* must be 1 or geater!'
    HEADER = 'Displaying {0} of {1} anime titles:'
    EMPTY_LIST = 'You have nothing in your anime list.'

    #argument processing
    file = FileList(filename)
    count = len(file)
    if num == None or num == '':
        num = count
    else:
        try:
            num = int(num)
        except ValueError:
            print(INT_ERROR)
            return
        if num < 1:
            print(NUM_ERROR)
            return
        elif count < num:
            num = count

    #check empty list
    if count < 1:
        print(EMPTY_LIST)
        return

    #display titles
    print(HEADER.format(num, count))
    for i in range(num):
        print(file[i])

def delete(filename: str, title: str):
    EMPTY_ERROR = '*anime_title* cannot be empty!'
    NOT_FOUND = 'Could not find "{0}"!'
    DELETE_SUCCESS = 'Removed "{0}" from your anime list.'

    if title == '':
        print(EMPTY_ERROR)
        return
    file = FileList(filename)
    pos = file.find(title)
    if pos == -1:
        print(NOT_FOUND.format(title))
    else:
        del file[pos]
        print(DELETE_SUCCESS.format(title))
        
if __name__ == '__main__':
    main()
