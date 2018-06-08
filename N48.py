from functools import lru_cache
import re


class Levenstein():

    FIND_WORD_PATTERN = re.compile(r'\w+')

    @staticmethod
    @lru_cache(maxsize=1024)
    def lev(s, t):
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
        return v1[len(t)]


    def find_it(self, find_word):

        res = filter(lambda x: (x[0] == find_word),self.correct_pair)
        try:
            res = res.__next__()
        except StopIteration:
            pass
        else:
            return res[1]

        up = False
        if find_word[0] != find_word[0].lower():
            up = True

        # формирование триграмм
        uWord = find_word.lower()
        word = ''
        part_uWord = uWord[:self.n_gramms].lower()
        sim = len(part_uWord)
        parts = []
        for x in self.parts.keys():
            nsim = Levenstein.lev(x, part_uWord)
            if nsim < self.n_gramms:
                parts.append(x)

        word = ''
        sim = len(uWord)
        for part in parts:
            for idx in range(self.parts[part][0],self.parts[part][1]+1):
                correct_word = self.dict[idx]
                nsim = Levenstein.lev(correct_word, uWord)
                if nsim < sim:
                    sim = nsim
                    return_word = correct_word
        if up:
            return_word = return_word.capitalize()
        if find_word != return_word:
            self.correct_pair.append((find_word,return_word))

        return return_word

    @staticmethod
    def read_text_gen(file_name):
        with open(file_name, 'r', encoding='cp1251') as file_obj: 
            while True: 
                row = file_obj.readline()
                if row: 
                    yield row 
                else: 
                    return
    @staticmethod
    def clear_file(file_name):
        with open(file_name, 'w', encoding='cp1251') as file_obj: 
            pass

    @staticmethod
    def load_dict(file_name):
        words = []
        parts = dict()
        with open(file_name, 'r', encoding='cp1251') as file_obj: 
            words = Levenstein.FIND_WORD_PATTERN.findall(file_obj.read())
            words.sort(key=lambda x: x)
            old_part = ''
            for idx, word in enumerate(words):
                part = word[:3].lower()
                if part not in parts.keys():
                    res = parts.get(old_part,None)
                    if res is not None:
                        parts[old_part] = (res[0],idx-1)
                    parts[part] = (idx,0)
                    old_part = part
        return {'words':words, 'parts':parts}

    def correct_text(self):
        self.correct_pair.clear()
        correct_row = ''
        results =  Levenstein.load_dict(self.dict_file)
        self.dict = results.get('words',[])
        self.parts = results.get('parts',dict())
        Levenstein.clear_file(self.correct_file)
        gen = Levenstein.read_text_gen(self.text_file)
        with open(self.correct_file, 'a', encoding='cp1251') as file_obj: 
            for row in gen:
                row = row.replace('\n','').strip()
                correct_row = row
                words = Levenstein.FIND_WORD_PATTERN.findall(row)
                for word in words:
                    correct_word = self.find_it(word)
                    correct_row = correct_row.replace(word,correct_word)
                print(f'{row} => {correct_row}')
                file_obj.write(f'{correct_row}\n')

    def __init__(self, n_gramms = 3, dict_file = 'dict.txt', text_file = 'text.txt', correct_file = 'correct.txt'):
        self.n_gramms = n_gramms
        self.dict_file = dict_file
        self.text_file = text_file
        self.correct_file = correct_file
        self.correct_pair = []
        self.dict = []
        self.parts = dict()

if __name__ == '__main__':
       Levenstein().correct_text()