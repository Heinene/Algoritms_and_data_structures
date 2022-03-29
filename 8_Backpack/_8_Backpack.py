import sys

class Item:
    def __init__(self, weight, cost):
        self.weight = weight
        self.cost = cost

class Backpack:
    @staticmethod
    def g(one, two):
        one = abs(one)
        two = abs(two)
        while one and two:
            if one >= two:
                one %= two
            else:
                two %= one
        return one | two

    def __init__(self, max_weight):
        self.__max_weight = max_weight
        self.__current_weight = 0
        self.__current_cost = 0
        self.__item_numbers = []

    def __get_coef(self, items):
        g = self.__max_weight
        for item in items:
            g = self.g(g, item.weight)
        return g or 1

    def __reduce_weights(self, items, g):
        for item in items:
            item.weight //= g
    
    def __return_weights(self, items, g):
        for item in items:
            item.weight *= g

    def __calc_table(self, n_rows, n_cols, items):
        table = [[0] * n_cols for _ in range(n_rows)]
        for i in range(1, n_rows):
            for j in range(n_cols):
                if items[i - 1].weight <= j\
                  and table[i - 1][j - items[i - 1].weight] + items[i - 1].cost > table[i - 1][j]:
                    table[i][j] = table[i - 1][j - items[i - 1].weight] + items[i - 1].cost
                else:
                    table[i][j] = table[i - 1][j]
        return table

    def __get_numbers(self, table, number, cur_weight, items):
        while table[number][cur_weight] > 0:
            if table[number - 1][cur_weight] != table[number][cur_weight]:
                self.__current_weight += items[number - 1].weight
                self.__item_numbers.append(number)
                cur_weight -= items[number - 1].weight
            number -= 1
        self.__item_numbers.reverse()

    def push_items(self, items):
        if len(items) == 0:
            return
        g = self.__get_coef(items)
        self.__reduce_weights(items, g)
        table = self.__calc_table(len(items) + 1, self.__max_weight // g + 1, items)
        self.__get_numbers(table, len(items), self.__max_weight // g, items)
        self.__current_weight *= g
        self.__current_cost = table[len(items)][self.__max_weight // g]
        self.__return_weights(items, g)

    def print_numbers(self, out):
        if self.__item_numbers:
            numbers = '\n'.join(str(number) for number in self.__item_numbers)
            out.write(f'{numbers}\n')
    
    def get_weight(self):
        return self.__current_weight
    
    def get_cost(self):
        return self.__current_cost


def parse_line(line):
    argv = line.split()
    number_one = int(argv[0])
    number_two = int(argv[1]) if len(argv) == 2 else None
    return number_one, number_two

maxweight = -1
for line in sys.stdin:
    if len(line) == 0 or line == '\n':
        continue
    try:
        maxweight, _ = parse_line(line)
        if maxweight >= 0:
            break
        print('error')
    except:
        print('error')
if maxweight < 0:
    quit()
items = []
for line in sys.stdin:
    if len(line) == 0 or line == '\n':
        continue
    try:
        weight, cost = parse_line(line)
        if weight >= 0 and cost >= 0:
            items.append(Item(weight, cost))
        else:
            print('error')
    except:
        print('error')
backpack = Backpack(maxweight)
backpack.push_items(items)
print(f'{backpack.get_weight()} {backpack.get_cost()}')
backpack.print_numbers(sys.stdout)