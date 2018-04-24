import re
import codecs
import chardet
import pandas as pd
import csv
from urllib.parse import urlparse, parse_qs


class Classification():

    def pars_row_(self, row):
        row = row.split('\t') #формируем список из строки
        query = urlparse(row[5]).query #ищем по параметрам get запроса
        query = parse_qs(query).get('text',['',])[0] #получаем параметр text
        query_set =  set(query.split(' '))

        intersection_words = self.word_set.intersection(query_set)
        intersection_stops = self.stop_set.intersection(query_set)

        #если нет совпадений с целевым множеством или
        #есть совпадения со множеством стоп-слов, то не создаем
        #строку
        row[5] = query
        if not intersection_words or intersection_stops: 
            return query_set
        intersection_len = len(intersection_words)

        row.append(str(intersection_len))
        row.append(','.join(list(query_set)))
        return row #pd.Series(row,index=self.columns) #создаем объект Series для загрузки в таблицу

    def read_row_gen_(self):
        with open(self.logfile,'rb') as f:
            rawdata = f.read(150) #читаем первые 30 символов для определения кодировки.
            result = chardet.detect(rawdata)
            encoding = result['encoding']

        with codecs.open(self.logfile, 'r', encoding=encoding) as tf:
            columns_ = tf.readline() #из шапки формируем имена колонок
            columns_ = columns_.split('\t')
            self.columns = [i.replace('\n','') for i in columns_] + ['intersection','query_set'] #добавляем колонку с количеством совпадений и уникальными значениясм
            #self.mainTable= pd.DataFrame(columns=self.columns)  #создаем пустую таблицу
            while True:
                line = tf.readline()
                if not line:
                    break
                try:
                    series = self.pars_row_(line)
                except:
                    pass
                yield series

    def readLog(self, max_line = None):
        if not self.word_set:
            print('word set is empty. Please use get_wordstat() first')
            return
        step = 1

        with open('first_result.csv', "w") as output:
            for row in self.read_row_gen_():

                #если задан предел обработки строк
                if max_line is not None:
                    if step >= max_line:
                        break

                if not isinstance(row,set):
                    print(f'{row[8]} - add to table')
                    writer = csv.writer(output,delimiter=';')
                    writer.writerows(row)
                    #row.T.to_csv('first_result.csv',sep =';',mode='a')
                    #self.mainTable = self.mainTable.append(row, ignore_index=True)
                    #self.mainTable.to_csv('data_frame.csv',sep =';')
                step += 1

    def create_set(self, filename):
        with open(filename,'rb') as f:
            rawdata = f.read(30) #читаем первые 30 символов для определения кодировки.
            result = chardet.detect(rawdata)
            encoding = result['encoding']

        with open(filename,'r',encoding=encoding) as f:
            words_ = self.word_pattern.findall(f.read())
        
        return_set = set()
        #создание список из всех слов
        retirn_list = [i.split(' ') for i in words_]
        #создание множества из всех слов
        [return_set.update(i) for i in retirn_list]
        return {'set':return_set, 'list':retirn_list}

    #заполнение целевых данных из файлов
    def get_wordset(self):
        self.word_set.clear()
        self.word_list.clear()
        result = self.create_set(self.wordstat)
        self.word_set = result['set']
        self.word_list = result['list']

        self.stop_list.clear()
        self.stop_set.clear()
        result = self.create_set(self.stopwords)
        self.stop_set = result['set']
        self.stop_list = result['list']

    def __init__(self, wordstat = 'words.txt', stopwords = 'stop.txt', log='Log'):
        self.word_pattern = re.compile(r'(.*)\n')

        #имена файлов
        self.wordstat = wordstat
        self.stopwords = stopwords
        self.logfile = log

        #переменные для хранения целевых данных в множестве
        self.word_set = set()
        self.stop_set = set()
        
        #переменные для хранения целевых данных в списке
        self.word_list = []
        self.stop_list = []

        #self.mainTable = None

A = Classification()
A.get_wordset()
A.readLog()
