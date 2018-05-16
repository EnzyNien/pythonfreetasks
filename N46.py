import re
import random
from collections import UserDict


class Synonyms():

    PATTERN = re.compile(r'(?P<key>\w+)\s*[-|—](?P<vals>.+)')

    def add_row_in_file(self, key, value):
        with open(self.filename, 'a') as f:
            f.write("{} - {}\n".format(key, value))

    def add_new(self, key):
        r = input('add new synonym to {} [y]es [n]o? '.format(key)).strip()
        if r.lower() == 'y' or r.lower() == 'yes':
            new_w = input('input new synonym => ').strip().lower()
            l = self.synonyms_dict[key]
            if new_w and (new_w not in l):
                l.append(new_w)
                self.synonyms_dict[key] = list(set(l))
                self.add_row_in_file(key, new_w)

    @property
    def make_work(self):
        while True:
            w = input('Please enter the word: ').strip()
            if w:
                w = w.lower()
                synonyms = self.synonyms_dict.get(w, None)
                if synonyms:
                    print('synonym: {}'.format(random.choice(synonyms)))
                    self.add_new(w)
                else:
                    print(
                        'the word for synonym search was not found in the dictionary\n')

    def make_values(self, val):
        return list(set([str(i).lower().strip()
                         for i in val.split(self.file_sep)]))

    '''
    synonyms.txt format
    word1 — synonym11; synonym12; synonym13;
    word2 — synonym2
    word3 — synonym3
    word4 — synonym4
    '''

    def __init__(self, filename='synonyms.txt', file_sep=';'):
        pattern = re.compile(r'(?P<key>\w+)\s*[-|—](?P<vals>.+)')

        self.filename = filename
        self.file_sep = file_sep
        self.synonyms_dict = UserDict()
        with open(filename, 'r') as f:
            synonyms = f.read()
            result = Synonyms.PATTERN.findall(synonyms)

        # collapse a list of tuples
        # optional procedure
        name_set = set([i[0] for i in result])
        tup_idx = [(i[0], idx) for idx, i in enumerate(result)]
        result_ = []
        for i in name_set:
            res = list(filter(lambda item: item[0] == i, tup_idx))
            '''
            result[idx[1]] = ('word1', ' synonym11; synonym12; synonym13;')
            result[idx[1]][1] = ' synonym11; synonym12; synonym13;'
            '''
            all_syn = [result[idx[1]][1] for idx in res]
            result_.append((i, ''.join(all_syn)))
        self.synonyms_dict = {
            item[0].lower(): self.make_values(
                item[1]) for item in result_}
        ##########################
        # or simple
        #self.synonyms_dict = {item[0].lower():self.make_values(item[1]) for item in result}

if __name__ == '__main__':
    Synonyms().make_work
