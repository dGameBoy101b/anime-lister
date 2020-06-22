#file io constants
FILE_SEP_CHAR = ','
FILE_STR_CHAR = '`'

#command parse constants
COM_SEP = ' '
CLOSE_COM = 'close'
HELP_COM = 'help'
ADD_COM = 'add'
VIEW_COM = 'view'
DELETE_COM = 'remove'
EDIT_COM = 'edit'
ADD_TAG_COM = 'tag'
DELETE_TAG_COM = 'untag'
LIST_TAGS_COM = 'tags'
TITLE_SEARCH_COM = 'title_search'
TAG_SEARCH_COM = 'tag_search'

def main():
    global COM_SEP, CLOSE_COM, HELP_COM, ADD_COM, VIEW_COM, DELETE_COM, LIST_TAGS_COM, TITLE_SEARCH_COM, TAG_SEARCH_COM
    PROMPT = '>>> '
    EDIT_PROMPT = 'EDIT "{0}"> '
    LIST_FILENAME = 'my_anime_list.csv'
    COM_ERROR = 'Command not recognised!'

    anime_list = load(LIST_FILENAME)
    editting = None
    aid()
    print()
    while True:
        if editting == None:
            com = input(PROMPT)
        else:
            for tag in anime_list[editting]:
                print(f'"{tag}"')
            com = input(EDIT_PROMPT.format(editting))
        if com == CLOSE_COM:
            save(anime_list, LIST_FILENAME)
            close()
        elif com == HELP_COM:
            aid()
        elif com.partition(COM_SEP)[0] == ADD_COM:
            anime_list = add(anime_list, com.partition(COM_SEP)[2])
            editting = None
        elif com.partition(COM_SEP)[0] == VIEW_COM:
            view(anime_list, com.partition(COM_SEP)[2])
            editting = None
        elif com.partition(COM_SEP)[0] == DELETE_COM:
            anime_list = delete(anime_list, com.partition(COM_SEP)[2])
            editting = None
        elif com.partition(COM_SEP)[0] == EDIT_COM:
            editting = edit(anime_list, editting, com.partition(COM_SEP)[2])
        elif com.partition(COM_SEP)[0] == ADD_TAG_COM:
            anime_list = add_tag(anime_list, editting, com.partition(COM_SEP)[2])
        elif com.partition(COM_SEP)[0] == DELETE_TAG_COM:
            anime_list = delete_tag(anime_list, editting, com.partition(COM_SEP)[2])
        elif com.partition(COM_SEP)[0] == LIST_TAGS_COM:
            list_tags(anime_list, com.partition(COM_SEP)[2])
            editting = None
        elif com.partition(COM_SEP)[0] == TITLE_SEARCH_COM:
            search_by_title(anime_list, com.partition(COM_SEP)[2])
            editting = None
        elif com.partition(COM_SEP)[0] == TAG_SEARCH_COM:
            search_by_tag(anime_list, com.partition(COM_SEP)[2])
            editting = None
        else:
            print(COM_ERROR)
        print()

def split_join(string: str, split: str, encase: str) -> [str]:
    parts = string.split(split)
    i = 0
    while i < len(parts) - 1:
        if parts[i].count(encase) % 2 != 0:
            parts = [parts[i] + parts[i + 1]] + parts[2:]
            continue
        i += 1
    return parts

def load(filename: str) -> {str: {str}}:
    global FILE_SEP_CHAR, FILE_STR_CHAR
    #open file
    try:
        file = open(filename, 'rt')
    except OSError:
        file.close()
        return dict()
    #read file
    anime_list = dict()
    while file.readable():
        line = file.readline()
        if line == '':
            break
        title = split_join(line.replace('\n', ''), FILE_SEP_CHAR, FILE_STR_CHAR)[0].replace(FILE_STR_CHAR, '')
        tags = split_join(line.replace('\n', ''), FILE_SEP_CHAR, FILE_STR_CHAR)[1:]
        for i in range(len(tags)):
            tags[i] = tags[i].replace(FILE_STR_CHAR, '')
        anime_list[title] = set(tags)
    file.close()
    return anime_list

def save(anime_list: {str: {str}}, filename: str):
    global FILE_SEP_CHAR, FILE_STR_CHAR
    #open file
    try:
        file = open(filename, 'wt')
    except OSError:
        file.close()
        return
    #read file
    for title in anime_list:
        line = ''
        line += f'{FILE_STR_CHAR}{title}{FILE_STR_CHAR}'
        for tag in anime_list[title]:
            line += f'{FILE_SEP_CHAR}{FILE_STR_CHAR}{tag}{FILE_STR_CHAR}'
        line += '\n'
        file.write(line)

def close():
    raise SystemExit

def aid():
    global COM_SEP, CLOSE_COM, HELP_COM, ADD_COM, VIEW_COM, DELETE_COM, EDIT_COM, ADD_TAG_COM, DELETE_TAG_COM, LIST_TAGS_COM, TITLE_SEARCH_COM, TAG_SEARCH_COM
    HELP_TEXT = (
        f'{CLOSE_COM}: close the program',
        f'{HELP_COM}: display this help text',
        f'{VIEW_COM}{COM_SEP}*max_items*: display titles on your anime list',
        '\t*max_items*: the maximum number of titles to display (leave blank for all titles)',
        f'{ADD_COM}{COM_SEP}*anime_title*: add an anime title to your list',
        '\t*anime_title*: the anime title you wish to add',
        f'{DELETE_COM}{COM_SEP}*anime_title*: remove an anime title from your list',
        '\t*anime_title*: the anime title you wish to remove',
        f'{EDIT_COM}{COM_SEP}*anime_title*: edit the tags of an anime title from your list',
        '\t*anime_title*: the anime title you wish to edit the tags of',
        f'{ADD_TAG_COM}{COM_SEP}*tag*: add a tag to the anime title being editted',
        '\t*tag*: the tag you wish to add to the anime title being editted',
        f'{DELETE_TAG_COM}{COM_SEP}*tag*: remove a tag from the anime title being editted',
        '\t*tag*: the tag you wish to remove from the anime title being edited',
        f'{LIST_TAGS_COM}{COM_SEP}*max_items*: display the tags in your anime list',
        '\t*max_items*: the maximum number of tags to display (leave blank for all tags)',
        f'{TITLE_SEARCH_COM}{COM_SEP}*title*: search for anime titles with a phrase in their title',
        '\t*title*: the phrase to search for in the titles of the animes in your list',
        f'{TAG_SEARCH_COM}{COM_SEP}*tag*: search for anime titles with a tag',
        '\t*tag*: the tag to search for',
        )
    
    #print help text
    for item in HELP_TEXT:
        print(item)

def add(anime_list: {str: {str}}, title: str) -> {str: {str}}:
    EMPTY_ERROR = '*anime_title* cannot be empty!'
    EXIST_ERROR = '"{0}" is already on your anime list!'
    ADD_SUCCESS = 'Added "{0}" to your anime list.'
    
    #check for empty title
    if title == '':
        print(EMPTY_ERROR)
        return anime_list
    
    #check for existing title
    if title in anime_list:
        print(EXIST_ERROR.format(title))
        return anime_list
    
    #add title to list
    anime_list[title] = set()
    print(ADD_SUCCESS.format(title))
    return anime_list

def display(anime_list: {str: {str}}, header: str = '', empty: str = '', num: int = None):
    #argument processing
    if not (isinstance(num, int) or num == None):
        raise TypeError(f'num must be an integer, not a {type(num)}!')
    if num == None:
        num = len(anime_list)
    elif num < 1 or num > len(anime_list):
        raise IndexError(f'num must be between 1 and {len(anime_list)}, not {num}!')
            
    #check empty list
    if len(anime_list) < 1:
        print(empty)
        return
    
    #display titles
    print(header.format(num, len(anime_list)))
    for i in range(num):
        print(f'"{list(anime_list.keys())[i]}"')

def view(anime_list: {str: {str}}, num: int = None):
    INT_ERROR = '*max_items* must be a number!'
    NUM_ERROR = '*max_items* must be 1 or greater!'
    HEADER = 'Displaying {0} of {1} anime titles:'
    EMPTY_LIST = 'You have nothing in your anime list.'

    #argument processing
    if num == '':
        num = None

    #display list
    try:
        display(anime_list, HEADER, EMPTY_LIST, num)
    except TypeError:
        print(NUM_ERROR)
    except IndexError:
        print(INT_ERROR)

def delete(anime_list: {str: {str}}, title: str) -> {str: {str}}:
    EMPTY_ERROR = '*anime_title* cannot be empty!'
    NOT_FOUND = 'Could not find "{0}"!'
    DELETE_SUCCESS = 'Removed "{0}" from your anime list.'
    
    #check empty title
    if title == '':
        print(EMPTY_ERROR)
        return anime_list
    
    #check for existing title
    if title not in anime_list:
        print(NOT_FOUND.format(title))
        return anime_list
    
    #remove title from list
    del anime_list[title]
    print(DELETE_SUCCESS.format(title))
    return anime_list

def edit(anime_list: {str: {str}}, editting: str, title: str) -> str:
    EMPTY_TITLE = '*anime_title* cannot be empty!'
    NOT_FOUND = 'Could not find "{0}"!'
    SUCCESS = 'Now editting the tags of "{0}".'
    
    #check empty title
    if title == '':
        print(EMPTY_TITLE)
        return editting
    
    #check existing title
    if title not in anime_list:
        print(NOT_FOUND.format(title))
        return editting
            
    #edit title
    print(SUCCESS.format(title))
    return title

def add_tag(anime_list: {str: {str}}, title: str, tag: str) -> {str: {str}}:
    EMPTY_TITLE = '*anime_title* cannot be empty!'
    EMPTY_TAG = '*tag* cannot be empty!'
    NOT_FOUND = 'Could not find "{0}"!'
    TAG_EXIST = '"{0}" already has the tag "{1}"!'
    SUCCESS = 'Added the tag "{1}" from "{0}".'
    
    #check empty title
    if title == '' or title == None:
        print(EMPTY_TITLE)
        return anime_list
    
    #check empty tag
    if tag == '' or title == None:
        print(EMPTY_TAG)
        return anime_list
        
    #check for existing title
    if title not in anime_list:
        print(NOT_FOUND.format(title))
        return anime_list
    
    #check for existing tag
    if tag in anime_list[title]:
        print(TAG_EXIST.format(title, tag))
        return anime_list
    
    #add tag
    anime_list[title].add(tag)
    print(SUCCESS.format(title, tag))
    return anime_list

def delete_tag(anime_list: {str: {str}}, title: str, tag: str) -> {str: {str}}:
    EMPTY_TITLE = '*anime_title* cannot be empty!'
    EMPTY_TAG = '*tag* cannot be empty!'
    NOT_FOUND = 'Could not find "{0}"!'
    TAG_NOT_EXIST = '"{0}" does not have the tag "{1}"!'
    SUCCESS = 'Removed the tag "{1}" from "{0}".'
    
    #check empty title
    if title == '' or title == None:
        print(EMPTY_TITLE)
        return anime_list
    
    #check empty tag
    if tag == '' or tag == None:
        print(EMPTY_TAG)
        return anime_list
    
    #check for existing title
    if title not in anime_list:
        print(NOT_FOUND.format(title))
        return anime_list
    
    #check for existing tag
    if tag not in anime_list[title]:
        print(TAG_NOT_EXIST)
        return anime_list
    
    #delete tag
    anime_list[title].remove(tag)
    print(SUCCESS.format(title, tag))
    return anime_list

def list_tags(anime_list: {str: {str}}, num: int = None):
    NO_TAGS = 'You have no tags in your anime list.'
    NUM_ERROR = '*max_items* must be 1 or greater!'
    HEADER = 'Displaying {0} of {1} tags:'
    
    #calculate tag list
    tags = set()
    for title in anime_list:
        tags = tags.union(anime_list[title])
        
    #check tags exist
    if len(tags) < 1:
        print(NO_TAGS)
        return
        
    #process max limit
    if num == None or num == '':
        num = len(tags)
    num = int(num)
    if num < 1:
        print(NUM_ERROR)
        return
        
    #display tags
    print(HEADER.format(num, len(tags)))
    for i in range(num):
        print(f'"{list(tags)[i]}"')

def search_by_title(anime_list: {str: {str}}, title: str, num: int = None):
    NO_MATCH = 'No title matches found for "{0}"!'
    HEADER = 'Displaying {1} of {2} results for "{0}" title search:'
    
    #find matches
    result = list()
    relevence = list()
    for i in range(len(anime_list)):
        if title in list(anime_list.keys())[i]:
            result.append(list(anime_list.keys())[i])
            relevence.append(len(list(anime_list.keys())[i].replace(title, '')))
    #sort by relevence
    for i in range(len(result)):
        for j in range(i + 1, len(result)):
            if relevence[j] < relevence[i]:
                temp = result[i]
                result[i] = result[j]
                result[j] = temp
                temp = relevence[i]
                relevence[i] = relevence[j]
                relevence[j] = temp
                
    #print results
    temp_anime_list = dict()
    for key in result:
        temp_anime_list[key] = anime_list[key]
    display(temp_anime_list, HEADER.format(title, '{0}', '{1}'), NO_MATCH.format(title), None)
    
def search_by_tag(anime_list: {str: {str}}, tag: str, num: int = None):
    NO_MATCH = 'No tag matches found for "{0}"!'
    HEADER = 'Displaying {1} of {2} results for "{0}" tag search:'
    
    #find matches
    result = list()
    for i in range(len(anime_list)):
        if tag in list(anime_list.values())[i]:
            result.append(list(anime_list.keys())[i])
    #print results
    temp_anime_list = dict()
    for key in result:
        temp_anime_list[key] = anime_list[key]
    display(temp_anime_list, HEADER.format(tag, '{0}', '{1}'), NO_MATCH.format(tag), None)
        
if __name__ == '__main__':
    main()
