from collections.abc import Iterable
from requests import request
from urllib.parse import urljoin, urlencode
import pandas as pd
import numpy as np
import uuid

from numbers import Number


class hh():

    DEFAULT_AREA = [113]
    API_URL = 'https://api.hh.ru/'
    PER_PAGE = 100

    SALARY_AREAS = '/salary_statistics/dictionaries/salary_areas'
    VACANCIES = 'vacancies'

    @classmethod
    def get_headers(cls):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://hh.ru',
            'Referer': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

    @classmethod
    def req(
            cls,
            method='get',
            headers=None,
            data=None,
            params=None,
            url=None,
            path=None):
        if url is None:
            url = hh.API_URL
        if path is None:
            path = hh.VACANCIES
        fullurl = urljoin(url, path)
        if headers is None:
            headers = hh.get_headers()
        encode_params = urlencode(dict() if params is None else params)
        encode_params = '?' + \
            encode_params if len(encode_params) else encode_params
        headers['Referer'] = fullurl + encode_params

        resp = request(
            method=method,
            url=fullurl,
            headers=headers,
            data=data,
            params=params)
        return resp

    @classmethod
    def pars_areas(cls, data):
        r_g = []
        if isinstance(data, dict):
            id = data.get('id', None)
            name = data.get('name', None)
            areas = data.get('areas', list())
            r_g = r_g + [(id, name)] + hh.pars_areas(areas)
            return r_g
        elif isinstance(data, list):
            r_l = []
            for row in data:
                r_l = r_l + hh.pars_areas(row)
            return r_l
        else:
            pass
        return r_g

    @classmethod
    def get_areas_id(cls):
        result = []
        resp = hh.req(path=hh.SALARY_AREAS)
        resp = resp.json()
        for row in resp:
            result += hh.pars_areas(row)
        result.sort(key=lambda x: x[0])
        return result


    def create_dfs(self):
        main_df_col = ['id',
                'name',
                'schedule',
                'published_at',
                'experience',
                'employment',
                'currency',
                'gross',
                'from',
                'to',
                'area',
                'employer_id',
                'employer_name']
        skills_df_col = ['id',
                        'name']
        spec_df_col = ['id',
                        'name']
        self.main_df = pd.DataFrame(columns = main_df_col)
        self.skills_df = pd.DataFrame(columns = skills_df_col)
        self.spec_df = pd.DataFrame(columns = spec_df_col)

    def compil_areas(self, areas):
        result = []
        for i in areas:
            try:
                result.append(('area', str(int(i))))
            except ValueError:
                try:
                    a = next(filter(lambda x: x[1] == i, self.areas_id))
                except StopIteration:
                    pass
                else:
                    result.append(('area', a[0]))
        return result

    def read_rows(self, rows):
        for row in rows:
            if row['archived'] or (self.main_df['id'] == row['id']).any():
                continue
            print(f"read {row['id']}")
            path = hh.VACANCIES + "/" + row['id']
            item = hh.req(path=path)
            if item.status_code is 200:
                item_j = item.json()
                main_df_dict = dict()
                _id = item_j['id']
                main_df_dict['schedule'] = item_j['schedule']['id']
                main_df_dict['published_at'] = item_j['published_at']
                main_df_dict['experience'] = item_j['experience']['id']
                main_df_dict['employment'] = item_j['employment']['id']
                main_df_dict['id'] = _id
                main_df_dict['currency'] = None
                main_df_dict['gross'] = None
                main_df_dict['from'] = None
                main_df_dict['to'] = None
                salary_ = item_j['salary']
                if salary_ is not None:
                    main_df_dict['currency'] = salary_.get('currency',None)
                    main_df_dict['gross'] = salary_.get('gross',None)
                    main_df_dict['from'] = salary_.get('from',None)
                    main_df_dict['to'] = salary_.get('to',None)
                main_df_dict['name'] = item_j['name']
                main_df_dict['employer_id'] = item_j['employer'].get('id',uuid.uuid4().hex)
                main_df_dict['employer_name'] = item_j['employer']['name']
                main_df_dict['area'] = item_j['area']['id']

                skills_df_list = [{'id':_id, 'name':i['name'].lower()} for i in item_j['key_skills']]
                spec_df_list = [{'id':_id, 'name':i['id']} for i in item_j['specializations']]

                self.main_df = self.main_df.append(pd.Series(main_df_dict), ignore_index=True)
                if skills_df_list:
                    self.skills_df = self.skills_df.append(skills_df_list, ignore_index=True)
                if spec_df_list:
                    self.spec_df = self.spec_df.append(spec_df_list, ignore_index=True)

    def get_data(self):
        self.vac_list.clear()
        global_params = [('text', self.title), ('per_page',
                                                self.PER_PAGE)] + self.compil_areas(self.areas_list)
        pages = 1
        page = 0
        while page <= pages:
            params = global_params.copy()
            params.append(('page', page))
            resp = self.req(params=params)
            if resp.status_code is 200:
                resp_j = resp.json()
                pages = resp_j['pages']
                self.read_rows(resp_j['items'])
                page += 1

    def __init__(self, title=None, areas_list=None):
        self.vac_list = []
        if areas_list is None:
            areas_list = []
        elif not isinstance(areas_list, Iterable):
            raise TypeError('areas_list must be list')
        elif not len(areas_list):
            self.areas_list = hh.DEFAULT_AREA
        else:
            self.areas_list = areas_list
        self.title = title if title is not None else ''
        self.areas_id = hh.get_areas_id()
        self.create_dfs()


if __name__ == '__main__':
    #areas_list=[
    #    'Москва',
    #    'Москва и Московская область',
    #    10002])
    data = hh(
        title='python',
        areas_list=['Москва',])
    data.get_data()
    
    #сохранение в json для примера
    data.main_df.to_json('main_df.json')
    data.skills_df.to_json('skills_df.json')
    data.spec_df.to_json('spec_df.json')