# -*- coding: utf-8 -*-
import re
import codecs
import chardet
import pandas as pd
from itertools import zip_longest


class Classification():

    @property
    def create_table(self):
        self.mainTable = pd.DataFrame(columns=self.columns)
        self.mainTable.to_csv(
            sep=',',
            header=True,
            index=False,
            mode='w',
            encoding='utf-8')

    @property
    def clear_table(self):
        self.mainTable.drop(self.mainTable.index, inplace=True)

    def compare(self, val, cmp):
        result = cmp.search(val)
        return 0 if result is None else len(result.groups())

    @staticmethod
    def clear_val(val):
        return val.lower().replace('\n', '')

    def pars_row_(self, row):
        row = ['', ] + row.split('\t')
        row = list(map(Classification.clear_val, row))
        row_dict = dict(zip_longest(self.columns, row, fillvalue=0))
        row_dict['req_cmp'] = 0

        req_word = self.compare(row_dict['request'], self.roots_w_ptrn)
        req_stop = self.compare(row_dict['request'], self.roots_s_ptrn)

        if req_stop > 0 or req_word == 0:
            return None
        row_dict['req_cmp'] = req_word
        return pd.Series(row_dict)

    def read_row_gen_(self):
        with open(self.logfile, 'rb') as f:
            # читаем первые 250 символов для определения кодировки.
            rawdata = f.read(250)
            result = chardet.detect(rawdata)
            encoding = result['encoding']

        with open(self.logfile, 'r', encoding=encoding) as tf:
            columns_ = tf.readline()  # из шапки формируем имена колонок
            columns_ = columns_.split('\t')
            self.columns = ['req_cmp', ] + \
                [i.replace('\n', '') for i in columns_]
            self.create_table
            while True:
                line = tf.readline()
                if not line:
                    break
                try:
                    series = self.pars_row_(line)
                except BaseException:
                    pass
                yield series

    def readLog(self, max_line=None, max_table_rows=300):
        if not self.roots_w_ptrn:
            print('roots pattern is empty. Please use get_word_pattern() first')
            return
        step = 1

        with open(self.result_file, 'w', encoding='utf-8') as f:
            pass

        for row in self.read_row_gen_():

            # если задан предел обработки строк
            if max_line is not None:
                if step >= max_line:
                    break

            if row is not None:
                pass
                if self.mainTable.shape[0] >= max_table_rows:
                    self.mainTable.to_csv(
                        self.result_file,
                        index=False,
                        header=False,
                        sep=',',
                        mode='a',
                        encoding='utf-8')
                    self.clear_table
                self.mainTable = self.mainTable.append(row, ignore_index=True)
            step += 1
        self.mainTable.to_csv(
            self.result_file,
            index=False,
            sep=',',
            header=False,
            mode='a',
            encoding='utf-8')

    def create_pattern(self, filename):
        with open(filename, 'rb') as f:
            rawdata = f.read(30)
            result = chardet.detect(rawdata)
            encoding = result['encoding']

        with open(filename, 'r', encoding=encoding) as f:
            words_ = self.word_pattern.findall(f.read())

        return_set = set()
        return_list = [i.split(' ') for i in words_]
        [return_set.update(i) for i in return_list]
        return_pattern = r'(' + '|'.join(list(return_set)) + ')'
        return return_pattern

    # заполнение целевых данных из файлов
    def get_word_pattern(self):
        self.roots_w_ptrn = re.compile(self.create_pattern(self.roots_w))
        self.roots_s_ptrn = re.compile(self.create_pattern(self.roots_s))
    '''
    req_words.txt must contain strings with the roots of the target words separated 
    by a shift of the page
    req_stop.txt must contain lines with the roots of stop words separated by a 
    shift of the page
    '''
    def __init__(
            self,
            roots_w='req_words.txt',
            roots_s='req_stop.txt',
            log='Log',
            result_file='data_frame.txt'):
        self.word_pattern = re.compile(r'(.*)\n')

        # имена файлов
        self.roots_w = roots_w
        self.roots_s = roots_s
        self.logfile = log
        self.result_file = result_file

        # переменные для хранения целевых данных
        self.roots_w_ptrn = ""
        self.roots_s_ptrn = ""

A = Classification()
A.get_word_pattern()
A.readLog(max_table_rows=50)
