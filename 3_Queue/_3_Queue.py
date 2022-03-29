import sys

class Queue:
    def __init__(self, max_size):
        self.__max_size = max_size
        self.__items = [0] * self.__max_size
        self.__size = 0
        self.__head = self.__tail = 0
    
    def push(self, item):
        if self.__size == self.__max_size:
            raise ValueError('overflow')
        self.__size += 1
        self.__items[self.__tail] = item
        self.__tail = (self.__tail + 1) % self.__max_size
    
    def pop(self):
        if self.__size == 0:
            raise ValueError('underflow')
        self.__size -= 1
        item = self.__items[self.__head]
        self.__head = (self.__head + 1) % self.__max_size
        return item
    
    def print(self, out):
        if self.__size == 0:
            out.write('empty\n')
            return
        out.write(f'{self.__items[self.__head]}')
        it = (self.__head + 1) % self.__max_size
        while it != self.__tail:
            out.write(f' {self.__items[it]}')
            it = (it + 1) % self.__max_size
        out.write('\n')

try:
    fin = open(sys.argv[1], 'r')
    fout = open(sys.argv[2], 'w')
except:
    quit()

queue = None
for line in fin:
    if len(line) == 0 or line == '\n':
        continue
    if line.startswith('set_size '):
        try:
            size = int(line[9:])
            if size >= 0:
                queue = Queue(size)
                break
        except:
            fout.write('error\n')
            continue
    fout.write('error\n')
if queue is None:
    quit()

for line in fin:
    line = line.strip('\n')
    if len(line) == 0:
        continue
    if line.startswith('push '):
        command = line.split()
        if len(command) == 2:
            try:
                queue.push(command[1])
            except ValueError as e:
                fout.write(f'{e}\n')
        else:
            fout.write('error\n')
    elif line == 'pop':
        try:
            fout.write(f'{queue.pop()}\n')
        except ValueError as e:
            fout.write(f'{e}\n')
    elif line == 'print':
        queue.print(fout)
    else:
        fout.write('error\n')
fin.close()
fout.close()