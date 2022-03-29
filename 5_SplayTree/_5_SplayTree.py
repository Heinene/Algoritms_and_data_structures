import sys

class SplayTree:
    class __SplayTreeNode:
        def __init__(self, key, data, parent=None):
            self._key = key
            self._data = data
            self._parent = parent
            self._left = None
            self._right = None
        
        def __str__(self):
            if self._parent is not None:
                return f'[{self._key} {str(self._data)} {self._parent._key}]'
            return f'[{self._key} {str(self._data)}]'
        
    def __init__(self):
        self.__root = None
    
    def __rotate(self, node, attr_one, attr_two):
        new_node = getattr(node, attr_one)
        new_node._parent = node._parent
        if new_node._parent is None:
            self.__root = new_node
        elif new_node._parent._left == node:
            new_node._parent._left = new_node
        else:
            new_node._parent._right = new_node
        node._parent = new_node
        mid_node = getattr(new_node, attr_two)
        setattr(new_node, attr_two, node)
        setattr(node, attr_one, mid_node)
        if mid_node is not None:
            mid_node._parent = node

    def __left_rotate(self, node):
        self.__rotate(node, '_right', '_left')
    
    def __right_rotate(self, node):
        self.__rotate(node, '_left', '_right')

    def __empty_rotate(self, node):
        if node._parent._left == node:
            self.__right_rotate(node._parent)
        else:
            self.__left_rotate(node._parent)

    def __full_rotate(self, node):
        if node == node._parent._left:
            if node._parent == node._parent._parent._left:
                self.__right_rotate(node._parent._parent)
                self.__right_rotate(node._parent)
            else:
                self.__right_rotate(node._parent)
                self.__left_rotate(node._parent)
        else:
            if node._parent == node._parent._parent._left:
                self.__left_rotate(node._parent)
                self.__right_rotate(node._parent)
            else:
                self.__left_rotate(node._parent._parent)
                self.__left_rotate(node._parent)

    def __splay(self, node):
        if node is not None:
            while node._parent is not None:
                if node._parent._parent is None:
                    self.__empty_rotate(node)
                else:
                    self.__full_rotate(node)
    
    def __splay_find_min_node(self, node):
        if node is not None:
            while node._left is not None:
                node = node._left
        self.__splay(node)
        return node
    
    def __splay_find_max_node(self, node):
        if node is not None:
            while node._right is not None:
                node = node._right
        self.__splay(node)
        return node

    def __splay_search_key_node(self, key, with_splay=True):
        node = self.__root
        while node is not None:
            if key < node._key:
                if node._left is None:
                    break
                node = node._left
            elif key > node._key:
                if node._right is None:
                    break
                node = node._right
            else:
                break
        if with_splay:
            self.__splay(node)
        return node
    
    def add(self, key, data):
        parent = self.__splay_search_key_node(key, False)
        if parent is None or parent._key != key:
            node = self.__SplayTreeNode(key, data, parent)
            if parent is None:
                self.__root = node
            elif parent._key > node._key:
                parent._left = node
            else:
                parent._right = node
            self.__splay(node)
            return True
        self.__splay(parent)
        return False

    def set(self, key, data):
        node = self.__splay_search_key_node(key)
        if node is not None and node._key == key:
            node._data = data
            return True
        return False
    
    def delete(self, key):
        node = self.__splay_search_key_node(key)
        if node is not None and node._key == key:
            if node._left is None and node._right is None:
                self.__root = None
            elif node._left is None:
                self.__root = node._right
                self.__root._parent = None
            elif node._right is None:
                self.__root = node._left
                self.__root._parent = None
            else:
                node._left._parent = node._right._parent = None
                self.__root = self.__splay_find_max_node(node._left)
                self.__root._right = node._right
                node._right._parent = self.__root
            return True
        return False

    def search(self, key):
        node = self.__splay_search_key_node(key)
        return node._data if node and key == node._key else None

    def min(self):
        node = self.__splay_find_min_node(self.__root)
        return node._key, node._data if node else None
    
    def max(self):
        node = self.__splay_find_max_node(self.__root)
        return node._key, node._data if node else None
    
    def empty(self):
        return self.__root is None
        
    def print(self, out):
        line = [self.__root if self.__root else '_']
        is_not_empty = True
        while is_not_empty:
            out.write(' '.join(str(node) for node in line))
            out.write('\n')
            next_line = []
            is_not_empty = False
            for node in line:
                if isinstance(node, self.__SplayTreeNode):
                    if node._left or node._right:
                        is_not_empty = True
                    next_line.append(node._left if node._left else '_')
                    next_line.append(node._right if node._right else '_')
                else:
                    next_line.append(f'{node} {node}')
            line = next_line


splay_tree = SplayTree()
for line in sys.stdin:
    line = line.strip()
    try:
        if line.startswith('add ') or line.startswith('set '):
            command, *key_data = line.split()
            key = int(key_data[0])
            data = key_data[1] if len(key_data) == 2 else ''
            if not getattr(splay_tree, command)(key, data):
                print('error')
        elif line.startswith('delete '):
            command, key = line.split()
            key = int(key)
            if not splay_tree.delete(key):
                print('error')
        elif line.startswith('search '):
            command, key = line.split()
            key = int(key)
            data = splay_tree.search(key)
            print(f'1 {data}' if data is not None else '0')
        elif line == 'min' or line == 'max':
            if not splay_tree.empty():
                key, data = getattr(splay_tree, line)()
                print(f'{key} {data}')
            else:
                print('error')
        elif line == 'print':
            splay_tree.print(sys.stdout)
        else:
            print('error')
    except:
        print('error')