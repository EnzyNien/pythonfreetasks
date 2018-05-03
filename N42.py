from requests import request
import re


class Instagram_FullHdPhoto():

    @staticmethod
    def get_full_hd_photo(id=''):
        full_url = f'https://i.instagram.com/api/v1/users/{id}/info/'
        resp = request('get', full_url)
        if resp.status_code == 200:
            resp_j = resp.json()
            '''['user'] -> ['hd_profile_pic_url_info'] ->  ['url']
                     -> ['hd_profile_pic_versions'] ->  [['url']]'''
            image_url = resp_j['user']['hd_profile_pic_url_info']['url']
            resp_url = request('get', image_url)
            if resp_url.status_code == 200:
                image_type = image_url.split('.')[-1]
                with open(f'id{id}.{image_type}', 'wb') as f:
                    f.write(resp_url.content)
                    print(f'download image from: {image_url}')
        else:
            print(f'download photo error.\n bad url: {photo_url}\n')

    @staticmethod
    def get_user_id(name, id_pattern):
        full_url = f'https://www.instagram.com/{name}/'
        resp = request('get', full_url)
        if resp.status_code == 200:
            id = id_pattern.search(resp.text)
            try:
                return id['id']
            except BaseException:
                print('id find error')
                return None
        else:
            return None

    def __init__(self, user_name=None):
        id_pattern = re.compile(r'profilePage_(?P<id>\d+)')
        if user_name is None:
            raise ValueError('user name must be str type')
        user_id = Instagram_FullHdPhoto.get_user_id(user_name, id_pattern)
        if user_id is not None:
            Instagram_FullHdPhoto.get_full_hd_photo(user_id)
        else:
            print('download photo error. user_id is None')


if __name__ == '__main__':
    Instagram_FullHdPhoto('schwarzenegger')
