from collections.abc import Iterable
from requests import request
from urllib.parse import urljoin, urlencode


from numbers import Number 



class hh():

    DEFAULT_AREA = [113]
    API_URL = 'https://api.hh.ru/'


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
    def req(cls, method='get', headers=None, data=None, params=None, url = None, path = None):
        if url is None:
            url = hh.API_URL
        if path is None:
            path = hh.VACANCIES
        fullurl = urljoin(url,path)
        if headers is None:
            headers = hh.get_headers()
        encode_params = urlencode(dict() if params is None else params)
        encode_params = '?' + encode_params if len(encode_params) else encode_params
        headers['Referer'] = fullurl + urlencode(encode_params)

        resp = request(method=method,url=fullurl,headers=headers,data=data,params=params)
        return resp

    @classmethod
    def pars_areas(cls,data):
        r_g = []
        if isinstance(data,dict):
            id = data.get('id',None)
            name = data.get('name',None)
            areas = data.get('areas',list())
            r_g = r_g + [(id,name)] + hh.pars_areas(areas)
            return r_g
        elif isinstance(data,list):
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
        resp = hh.req(path = hh.SALARY_AREAS)
        resp = resp.json()
        for row in resp:
            result += hh.pars_areas(row)
        result.sort(key=lambda x:x[0])
        return result

    def compil_areas(self,areas):
        for i in areas:
            try:
                i = int(i)
            except ValueError:
                pass

    def get_data(self):
        params = {'text':self.title,
                  'area':self.compil_areas(self.areas)}
        resp = self.req

    def __init__(self, title=None, areas_list=None):
        if areas_list is None:
            areas_list = []
        elif not isinstance(areas_list,Iterable):
            raise TypeError('areas_list must be list')
        elif not len(areas_list):
            self.areas_list = hh.DEFAULT_AREA
        else:
            self.areas_list = areas_list
        self.title = titel if title is not None else ''
        self.areas_id = hh.get_areas_id()

a = hh()
a.get_data()

