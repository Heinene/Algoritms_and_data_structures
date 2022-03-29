import sys
from math import log2, log
from array import array

class BitSet:
    def __init__(self, size, bit_set_type='Q'):
        if bit_set_type == 'Q':
            self.__type_size = 64
        elif bit_set_type == 'L':
            self.__type_size = 32
        elif bit_set_type == 'I':
            self.__type_size = 16
        else:
            bit_set_type = 'B'
            self.__type_size = 8
        self.__size = size
        self.__capacity = (self.__size + self.__type_size - 1) // self.__type_size
        self.__set = array(bit_set_type, (0b0 for _ in range(self.__capacity)))

    def __getitem__(self, key):
        set_pos, bit_pos = divmod(key, self.__type_size)
        return (self.__set[set_pos] >> (self.__type_size - 1 - bit_pos)) & 0b1
    
    def __setitem__(self, key, value):
        set_pos, bit_pos = divmod(key, self.__type_size)
        if value:
            self.__set[set_pos] |= (1 << (self.__type_size - 1 - bit_pos))
        else:
            self.__set[set_pos] = ~((~self.__set[set_pos]) | (1 << (self.__type_size - 1 - bit_pos)))

    def __str__(self):
        return ''.join(str(self[bit]) for bit in range(self.__size))


class BloomFilter:
    MersenThirtyOne = 2147483647

    def __init__(self, size, probability):
        if size <= 0 or probability <= 0 or probability > 1.0 / (2.0 ** 0.5):
            raise ValueError('wrong paramets')
        self.__number_hashers = round(-log2(probability))
        self.__size = round(-size * log2(probability) / log(2))
        self.__primes = self.__get_primes()
        self.__bit_set = BitSet(self.__size)

    def __str__(self):
        return str(self.__bit_set)

    def __get_primes(self):
        prime_numbers = [2] * self.__number_hashers
        test_number = 3
        pos = 1
        while pos < self.__number_hashers:
            is_prime = True
            for i in range(1, pos):
                if test_number % prime_numbers[i] == 0:
                    is_prime = False
                    break
            if is_prime:
                prime_numbers[pos] = test_number
                pos += 1
            test_number += 2
        return prime_numbers

    def __hasher(self, i, key):
        key %= self.MersenThirtyOne
        return (((i + 1) * key + self.__primes[i]) % self.MersenThirtyOne) % self.__size

    def add(self, key):
        for i in range(self.__number_hashers):
            self.__bit_set[self.__hasher(i, key)] = 0b1

    def search(self, key):
        for i in range(self.__number_hashers):
            if self.__bit_set[self.__hasher(i, key)] == 0b0:
                return False
        return True
    
    def get_size(self):
        return self.__size
    
    def get_number_hashers(self):
        return self.__number_hashers


def parse_line(line):
    argv = line.split()
    command = argv[0]
    key = int(argv[1]) if len(argv) > 1 else None
    probability = float(argv[2]) if len(argv) > 2 else None
    return command, key, probability

filter = None
for line in sys.stdin:
    if line == '\n' or len(line) == 0:
        continue
    try:
        command, size, probability = parse_line(line)
        if command == 'set' and size is not None and probability is not None:
            filter = BloomFilter(size, probability)
            print(f'{filter.get_size()} {filter.get_number_hashers()}')
            break
        print('error')
    except:
        print('error') 

for line in sys.stdin:
    if line == '\n' or len(line) == 0:
        continue
    try:
        command, key, _ = parse_line(line)
        if command == 'add':
            filter.add(key)
        elif command == 'search':
            print('1' if filter.search(key) else '0')
        elif command == 'print':
            print(filter)
        else:
            print('error')
    except:
        print('error')