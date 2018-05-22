import re
from random import uniform
from collections import defaultdict


class Markov():

    ALPH = re.compile(r'[а-яА-Я0-9-]+|[.,:;?!]+')

    def gen_get_lines(self):
        with open(self.filename, 'r') as data:
            for line in data:
                yield line.lower()

    def gen_make_tokens(self, lines):
        for line in lines:
            for token in Markov.ALPH.findall(line):
                yield token

    def gen_trigrams(self, tokens):
        t0, t1 = ['$'] * 2
        for t2 in tokens:
            yield t0, t1, t2
            if t2 in '.!?':
                yield t1, t2, '$'
                yield t2, '$', '$'
                t0, t1 = '$', '$'
            else:
                t0, t1 = t1, t2

    def pocess(self):
        lines = self.gen_get_lines()
        tokens = self.gen_make_tokens(lines)
        _trigrams = self.gen_trigrams(tokens)

        bi = defaultdict(lambda: float(0))
        tri = defaultdict(lambda: float(0))

        for t0, t1, t2 in _trigrams:
            bi[t0, t1] += 1
            tri[t0, t1, t2] += 1

        self.model.clear()
        for (t0, t1, t2), freq in tri.items():
            if (t0, t1) in self.model:
                self.model[t0, t1].append((t2, freq / bi[t0, t1]))
            else:
                self.model[t0, t1] = [(t2, freq / bi[t0, t1])]
        return self

    def unirandom(self, seq):
        sum_, freq_ = 0, 0
        for item, freq in seq:
            sum_ += freq
        rnd = uniform(0, sum_)
        for token, freq in seq:
            freq_ += freq
            if rnd < freq_:
                return token

    def sentences(self):
        phrase = ''
        t0, t1 = '$', '$'
        while True:
            t0, t1 = t1, self.unirandom(self.model[t0, t1])
            if t1 == '$':
                break
            if t1 in ('.!?,;:') or t0 == '$':
                phrase += t1
            else:
                phrase += ' ' + t1
        return phrase.capitalize()

    def display(self, count=3):
        for i in range(count):
            print(self.sentences())

    def __init__(self, filename='dub.txt'):
        self.filename = filename
        self.model = dict()


if __name__ == '__main__':
    chain = Markov().pocess()
    chain.display(5)
