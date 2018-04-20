from requests import request
import json


class Tradingview():

    URL = 'https://scanner.tradingview.com/crypto/scan'

    @staticmethod
    def get_headers():
        return {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "696",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "scanner.tradingview.com",
            "Origin": "https://ru.tradingview.com",
            "Referer": "https://ru.tradingview.com/cryptocurrency-signals/",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    @staticmethod
    def api_query(data):
        req = request(
            'post',
            url=Tradingview.URL,
            data=data,
            headers=Tradingview.get_headers())
        try:
            result = req.json()
        except:
            result = None
        finally:
            return result

    @staticmethod
    def returnJson():
        filters_ = {"filter": [{"left": "change",
                                    "operation": "nempty"},
                                   {"left": "change",
                                    "operation": "greater",
                                    "right": 0},
                                   {"left": "Recommend.All",
                                    "operation": "nequal",
                                    "right": 0}],
                        "filter2": {"operator": "and",
                                    "operands": [{"operation": {"operator": "or",
                                                                "operands": [{"expression": {"left": "Recommend.All",
                                                                                             "operation": "in_range",
                                                                                             "right": [0,
                                                                                                       0.5]}},
                                                                             {"expression": {"left": "Recommend.All",
                                                                                             "operation": "in_range",
                                                                                             "right": [0.5,
                                                                                                       1]}}]}}]},
                        "symbols": {"query": {"types": []}},
                        "columns": ["name",
                                    "close",
                                    "change",
                                    "change_abs",
                                    "high",
                                    "low",
                                    "volume",
                                    "Recommend.All",
                                    "exchange",
                                    "description",
                                    "name",
                                    "subtype",
                                    "pricescale",
                                    "minmov",
                                    "fractional",
                                    "minmove2"],
                        "sort": {"sortBy": "change",
                                 "sortOrder": "desc"},
                        "options": {"lang": "ru"},
                        "range": []}

        data = json.dumps(filters_)
        return Tradingview.api_query(data)

if __name__ == '__main__':
    result = Tradingview.returnJson()
