# -*- coding: utf-8 -*-
import codecs
import re
import csv
from openpyxl import Workbook
from collections import OrderedDict as OD


class YandexLog():

    def in_lists(self, value, cmp_list):
        compare = 0
        # ищем вхождение слов из списка
        # если вхождения есть - добавляем единицу к результату
        for i in cmp_list:
            if i in value:
                compare += 1
        return compare

    # процедура инициализации списков слов
    def create_lists(self):
        self.request_list = ['тв',
                             'телев',
                             'сери',
                             'кино',
                             'стс',
                             'тнт',
                             'дождь',
                             'домашний',
                             'канал',
                             'пятница',
                             'шоу',
                             'мульт',
                             'tv',
                             'триколор',
                             'спутнико',
                             'програм',
                             'передач',
                             'фильм',
                             'трансляц',
                             'смотреть',
                             'сезон',
                             ]
        self.request_stop_list = [
            'порно',
            'секс',
            'инцест',
            'тверь',
            'твор',
            'молитв',
            'ств',
            'мертв',
            'отве',
            'магаз',
            'тво',
            'битв',
            'матве',
            'тви',
            'посмотр',
            'рестс',
            'качеств',
        ]
        self.url_list = [
            'tv',
            'kino',
            'serial',
            'telev',
            'tnt-online.ru',
            'videomore.ru',
            'domashniy.ru',
            'friday.ru',
            'ctc.ru',
            'matchboets',
        ]
        self.url_stop_list = [
            'porn',
            'xxx',
            'otvet,'
            'estv',
            'tver',
            'latvi',
            'tsveta',
            'xvideo',
            'stv',
            'tvoy',
            'tvoi',
        ]

    # процедура обработки текущей строки файла лога
    def pars_row_(self, row):
        row = row.lower()  # приведение к нижнему регистру
        timestamp, datetime, device, numdoc, region, request, urls, * \
            a = row.split('\t')

        # проверки вхождений:
        request_ok = self.in_lists(request, self.request_list)
        request_bad = self.in_lists(request, self.request_stop_list)

        url_ok = self.in_lists(urls, self.url_list)
        url_bad = self.in_lists(urls, self.url_stop_list)

        # пропускаем значения со стоп словами
        if request_bad > 0 or url_bad > 0 or (request_ok == 0 and url_ok == 0):
            return None

        # формируем словарь с результатом
        return_dict = OD.fromkeys(self.keys, None)
        return_dict['timestamp'] = timestamp
        return_dict['datetime'] = datetime
        return_dict['device'] = device
        return_dict['numdoc'] = numdoc
        return_dict['region'] = region
        return_dict['request'] = request
        return_dict['urls'] = urls
        return_dict['request_ok'] = request_ok
        return_dict['url_ok'] = url_ok
        return return_dict

    # предварительно создаем три пустых файла с результатами
    def create_csv(self):
        with codecs.open(self.result_request, "w", encoding='utf-8') as f:
            heads = csv.DictWriter(f, fieldnames=self.keys)
            heads.writeheader()
        with codecs.open(self.result_urls, "w", encoding='utf-8') as f:
            heads = csv.DictWriter(f, fieldnames=self.keys)
            heads.writeheader()
        with codecs.open(self.result_all, "w", encoding='utf-8') as f:
            heads = csv.DictWriter(f, fieldnames=self.keys)
            heads.writeheader()

    def add_row_to_csv(self, filename, row):
        with codecs.open(filename, "a", encoding='utf-8') as f:
            heads = csv.DictWriter(f, fieldnames=self.keys)
            heads.writerow(row)

    # процедура построчного чтения файла лога
    def read_row_gen_(self):
        with codecs.open(self.logfile, "r", "utf-8") as f:
            keys_ = f.readline()  # из шапки формируем имена колонок
            keys_ = keys_.split('\t')

            self.keys = [i.replace('\n', '')
                         for i in keys_] + ['request_ok', 'url_ok']
            self.create_csv()
            while True:
                line = f.readline()
                if not line:
                    break
                try:
                    series = self.pars_row_(line)
                except BaseException:
                    pass
                yield series

    def read_log(self, max_line=None):
        step = 1
        request_ok_rows = 0
        url_ok_rows = 0
        result_all_rows = 0
        for row in self.read_row_gen_():

            # если задан предел обработки строк
            if max_line is not None:
                if step >= max_line:
                    break

            if row is None:
                step += 1
                continue

            # пишем в result_request
            if row['request_ok'] > 0:
                self.add_row_to_csv(self.result_request, row)
                request_ok_rows += 1

            # пишем в result_urls
            if row['url_ok'] > 0:
                self.add_row_to_csv(self.result_urls, row)
                url_ok_rows += 1

            # пишем в result_all
            if row['request_ok'] > 0 and row['url_ok'] > 0:
                self.add_row_to_csv(self.result_all, row)
                result_all_rows += 1

            step += 1

        print('RESULTS:')
        print(f'ALL ROWS: {step}')
        print(
            f'request cmp rows: {request_ok_rows} ({request_ok_rows/step*100:.2f}%)')
        print(f'url cmp rows: {url_ok_rows} ({url_ok_rows/step*100:.2f}%)')
        print(
            f'all cmp rows: {result_all_rows} ({result_all_rows/step*100:.2f}%)')

    def __init__(
            self,
            logfile='Log',
            result_request='result_request.txt',
            result_urls='result_urls.txt',
            result_all='result_all.txt'):
        self.logfile = logfile
        self.result_request = result_request
        self.result_urls = result_urls
        self.result_all = result_all
        self.create_lists()


YandexLog().read_log()
