import os

class FileList():

    def __init__(self, filename: str, iterable: [str] = []):
        #check parameter types
        if not isinstance(filename, str):
            raise TypeError('filename must be a string')
        try:
            iter(iterable)
        except TypeError:
            raise TypeError('iterable must be iterable')

        #set instance variables
        self.filename = filename

        #create file
        try:
            open(filename, mode='xt').close()
        except FileExistsError:
            pass

        #add iterables
        for item in iterable:
            self.append(item)

    def __repr__(self) -> str:
        return f'FileList({self.filename!r})'

    def __len__(self) -> int:
        file = open(self.filename, mode='rt')
        count = 0
        while True:
            line = file.readline()
            if line == '':
                break
            count += 1
        file.close()
        return count

    def __getitem__(self, index: int) -> str:
        #check parameter type
        if not isinstance(index, (int, slice)):
            raise TypeError('index must an integer or a slice')
        
        #handle integer index
        if isinstance(index, int):
            #check index range
            if index < 0:
                index += len(self)
            if index < 0 or index >= len(self):
                raise IndexError

            #skip pre-index items
            file = open(self.filename, mode='rt')
            for i in range(index):
                file.readline()

            #retreive index item
            item = file.readline()
            file.close()
            return item[:-1]
        
        #handle slice index
        file = open(self.filename, mode='rt')
        count = 0
        items = list()
        for i in index.indicies(len(self)):

            #skip non-index items
            while count < i:
                file.readline()
                count += 1

            #retreive index item
            items.append(file.readline()[:-1])
            count += 1
            
        return items

    def __setitem__(self, index: int, value: str):
        #check parameter types
        if not isinstance(index, int):
            raise TypeError('index must be an integer')
        if not isinstance(value, str):
            raise TypeError('value must be a string')
        if '\n' in value:
            raise ValueError('value must not contain "\\n"')

        #check index range
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError

        #copy pre-index items to temporary file
        file = open(self.filename, mode='rt')
        temp_file = open(self.filename + '.tmp', mode='w+t')
        for i in range(index):
            print(file.readline(), file=temp_file, end='')

        #insert value into temporary file
        print(value, file=temp_file, end='')
        file.readline()

        #copy post-index items to temporary file
        count = len(self)
        for i in range(count - index - 1):
            print(file.readline(), file=temp_file)
        file.close()

        #copy temporary file contents to file
        file = open(self.filename, mode='wt')
        temp_file.seek(0)
        for i in range(count):
            print(temp_file.readline(), file=file, end='')
        file.close()
        
        #clean up temporary file
        temp_file.close()
        os.remove(os.path.abspath(self.filename + '.tmp'))

    def __delitem__(self, index: int):
        #check parameter type
        if not isinstance(index, int):
            raise TypeError('index must be an integer')

        #check index range
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError
        
        #copy pre-index items to temporary file
        file = open(self.filename, mode='rt')
        temp_file = open(self.filename + '.tmp', mode='w+t')
        for i in range(index):
            print(file.readline(), file=temp_file, end='')

        #skip index item
        file.readline()

        #copy post-index item to temporary file
        count = len(self) - 1
        for i in range(count - index):
            print(file.readline(), file=temp_file, end='')
        file.close()

        #copy temporary file contents to file
        file = open(self.filename, mode='wt')
        temp_file.seek(0)
        for i in range(count):
            print(temp_file.readline(), file=file, end='')

        #clean up temporary file
        temp_file.close()
        os.remove(os.path.abspath(self.filename + '.tmp'))

    def __iter__(self) -> iter:
        return iter(self[:])
            
    def append(self, value: str):
        #check parameter type
        if not isinstance(value, str):
            raise TypeError('value must be a string')
        if '\n' in value:
            raise ValueError('value must not contain "\\n"')

        #append value
        file = open(self.filename, mode='at')
        print(value, file=file)
        file.close()

    def find(self, value: str, start: int = 0, end: int = None) -> int:
        #check parameter types
        if not isinstance(value, str):
            raise TypeError('value must be a string')
        if not isinstance(start, int):
            raise TypeError('start must be an integer')
        if end == None:
            end = len(self)
        if not isinstance(end, int):
            raise TypeError('end must be an integer')

        #search for value
        for i in range(start, end):
            if self[i] == value:
                return i
        return -1
