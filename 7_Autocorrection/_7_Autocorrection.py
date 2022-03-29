import sys

class Trie:
    class __TrieNode:
        def __init__(self):
            self._children = dict()
            self._is_word = False

    def __init__(self):
        self.__root = self.__TrieNode()

    #  Проверяет есть ли слово в дереве
    #  Сложность: O(|word|)
    #  Идем по слову и параллельно спускаемся по дереву
    #  Если символа не оказалось на текущей ветке, то нужного слова - нет
    #  Иначе, спускаемся на уровень ниже
    #  В итоге мы либо дойдем до конца слова, либо прервёмся на первом символе,
    #  которого нет в дереве, отсюда и сложность
    def __contains__(self, word, it=None):
        if it is None:
            word = word.lower()
            it = self.__root
        for letter in word:
            if letter not in it._children:
                return False
            it = it._children[letter]
        return it._is_word
    
    #  Добавляет слово в дерево
    #  Сложность: O(|word|)
    #  Идем по слову и параллельно спускаемся по дереву
    #  Если символа не оказалось на текущей ветке, то добавляем звено
    #  Иначе, спускаемся на уровень ниже
    #  В итоге мы пройдем целиком по слову, отсюда и сложность
    def add(self, word):
        word = word.lower()
        it = self.__root
        for letter in word:
            if letter not in it._children:
                it._children[letter] = self.__TrieNode()
            it = it._children[letter]
        it._is_word = True    

    #  Находит похожие слова (слова, полученные из word исправлением одной ошибки)
    #  Сложность O(|word|^3)
    #  Мы идём по строке и параллельно спускаемся по дереву
    #  Если мы достигли конца строки или дальнейший спуск по дереву невозможен - прерываемся
    #  Сложность прохода по строке O(|word|)
    #  Для каждого символа, мы применяем одну из операций (Удаление/Замена/Вставка/Перестановка)
    #   Операция удаления - сложность: O(|word|), т.к нужно проверить, что слово в словаре
    #   Операция перестановки - сложность: O(|word|), аналогично удалению
    #   Операция замены - сложность: O(|word|*|Children|), т.к мы заменяем текущий символ
    #       на каждого из потомков и для каждого такого варианта, проверяем есть ли слово в словаре
    #   Операция втавки - сложность: O(|word|*|Children|), аналогично замене
    #  Суммарная сложность операций:
    #   O(|word| * (|word|*|Children1| + |word|*|Children2| + ... + |word|*|ChildrenN|)) =
    #   = {обозначим количество детей для вершины за константу C} =
    #   = O(|word|^2 * C * |word|) = O(|word|^3)
    #  Сложность сортировки: O(N*ln(N)*|word|), где N - количество слов
    #   N = {на каждый символ исх. слова, можем добавить 1 + |Children|} = |word| * (1 + |Сhildren|) =>
    #   => O(N*ln(N)*|word|) = O(|word|^2 * ln(|word|))
    #  Сложность алгоритма: O(|word|^3 + |word|^2 * ln(|word|)) = O(|word|^3)
    def search_like_words(self, word):
        word = word.lower()
        words = []
        it = self.__root
        for pos in range(len(word) + 1):
            if pos + 1 <= len(word) and (pos == 0 or word[pos] != word[pos - 1])\
              and self.__contains__(word[pos + 1:], it):
                words.append(f'{word[:pos]}{word[pos + 1:]}')
            ch = word[pos:pos + 1]
            if pos + 1 < len(word) and word[pos + 1] in it._children\
              and ch in it._children[word[pos + 1]]._children\
              and self.__contains__(word[pos + 2:], it._children[word[pos + 1]]._children[ch]):
                words.append(f'{word[:pos]}{word[pos + 1]}{ch}{word[pos + 2:]}')
            for child in it._children:
                if ch == child:
                    continue
                if self.__contains__(word[pos + 1:], it._children[child]):
                    words.append(f'{word[:pos]}{child}{word[pos + 1:]}')
                if ch in it._children[child]._children\
                  and self.__contains__(word[pos + 1:], it._children[child]._children[ch]):
                    words.append(f'{word[:pos]}{child}{ch}{word[pos + 1:]}')
            if pos < len(word) and word[pos] in it._children:
                it = it._children[word[pos]]
            else:
                break
        return sorted(words)


sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

trie = Trie()
number_words = int(input())
for i in range(number_words):
    trie.add(input())

for word in sys.stdin:
    word = word.strip('\n')
    if len(word) == 0:
        continue
    if word in trie:
        print(f'{word} - ok')
    else:
        words = trie.search_like_words(word)
        print(f'{word} -> {", ".join(words)}' if words else f'{word} -?')
