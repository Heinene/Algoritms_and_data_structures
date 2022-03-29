import sys

class KeyHeap:
    class __KeyHeapNode:
        def __init__(self, key, data):
            self._key = key
            self._data = data

        def _to_str(self, parent_key=None):
            if parent_key is not None:
                return f'[{self._key} {self._data} {parent_key}]'
            return f'[{self._key} {self._data}]'

    def __init__(self):
        self.__nodes = []
        self.__node_keys = dict()
    
    def __len__(self):
        return len(self.__nodes)
    
    def __swap(self, node_one, node_two):
        key_one = self.__nodes[node_one]._key
        key_two = self.__nodes[node_two]._key
        swap_index = self.__node_keys[key_one]
        self.__node_keys[key_one] = self.__node_keys[key_two]
        self.__node_keys[key_two] = swap_index
        swap_node = self.__nodes[node_one]
        self.__nodes[node_one] = self.__nodes[node_two]
        self.__nodes[node_two] = swap_node

    def __sift_down(self, node):
        while node * 2 + 1 < len(self.__nodes):
            left_node = node * 2 + 1
            right_node = node * 2 + 2
            min_node = left_node
            if right_node < len(self.__nodes) and self.__nodes[right_node]._key < self.__nodes[left_node]._key:
                min_node = right_node
            if self.__nodes[node]._key <= self.__nodes[min_node]._key:
                break
            self.__swap(min_node, node)
            node = min_node
    
    def __sift_up(self, node):
        while node > 0 and self.__nodes[node]._key < self.__nodes[(node - 1) // 2]._key:
            self.__swap(node, (node - 1) // 2)
            node = (node - 1) // 2
    
    def add(self, key, data):
        if key in self.__node_keys:
            return False
        self.__nodes.append(self.__KeyHeapNode(key, data))
        self.__node_keys[key] = len(self.__nodes) - 1
        self.__sift_up(len(self.__nodes) - 1)
        return True
    
    def set(self, key, data):
        if key not in self.__node_keys:
            return False
        node = self.__node_keys[key]
        self.__nodes[node]._data = data
        return True

    def delete(self, key):
        if key not in self.__node_keys:
            return False
        node = self.__node_keys[key]
        self.__swap(node, len(self.__nodes) - 1)
        self.__nodes.pop()
        self.__node_keys.pop(key)
        if node < len(self.__nodes):
            self.__sift_down(node)
            self.__sift_up(node)
        return True

    def search(self, key):
        if key not in self.__node_keys:
            return None
        node = self.__node_keys[key]
        result = self.__nodes[node]
        return result._data, node

    def min(self):
        if len(self.__nodes) == 0:
            return None
        result = self.__nodes[0]
        return result._key, result._data, 0
    
    def max(self):
        if len(self.__nodes) == 0:
            return None
        max_node = 0
        for node in range(len(self.__nodes) // 2, len(self.__nodes)):
            if self.__nodes[node]._key > self.__nodes[max_node]._key:
                max_node = node
        result = self.__nodes[max_node]
        return result._key, result._data, max_node

    def extract(self):
        if len(self.__nodes) == 0:
            return None
        result = self.__nodes[0]
        self.__swap(0, len(self.__nodes) - 1)
        self.__nodes.pop()
        self.__node_keys.pop(result._key)
        self.__sift_down(0)
        return result._key, result._data

    def print(self, out):
        out.write(self.__nodes[0]._to_str() + '\n' if len(self.__nodes) else '_\n')
        left_node = 1
        right_node = 2
        while left_node < len(self.__nodes):
            line = []
            for node in range(left_node, min(right_node + 1, len(self.__nodes))):
                line.append(self.__nodes[node]._to_str(self.__nodes[(node - 1) // 2]._key))
            if right_node >= len(self.__nodes):
                line.append(' '.join(('_' for i in range(right_node - len(self.__nodes) + 1))))
            out.write(' '.join(line))
            out.write('\n')
            left_node = 2 * left_node + 1
            right_node = 2 * right_node + 2


def parse_line(line):
    argv = line.split()
    command = argv[0]
    key = int(argv[1]) if len(argv) > 1 else None
    data = argv[2] if len(argv) > 2 else None
    return command, key, data

key_heap = KeyHeap()

for line in sys.stdin:
    command, key, data = parse_line(line)
    if command == 'add':
        if not key_heap.add(key, data):
            print('error')
    elif command == 'set':
        if not key_heap.set(key, data):
            print('error')
    elif command == 'delete':
        if not key_heap.delete(key):
            print('error')
    elif command == 'search':
        result = key_heap.search(key)
        if result is not None:
            data, index = result
            print(f'1 {index} {data}')
        else:
            print('0')
    elif command == 'min':
        if len(key_heap) != 0:
            key, data, index = key_heap.min()
            print(f'{key} {index} {data}')
        else:
            print('error')
    elif command == 'max':
        if len(key_heap) != 0:
            key, data, index = key_heap.max()
            print(f'{key} {index} {data}')
        else:
            print('error')
    elif command == 'extract':
        if len(key_heap) != 0:
            key, data = key_heap.extract()
            print(f'{key} {data}')
        else:
            print('error')
    elif command == 'print':
        key_heap.print(sys.stdout)