from requests import request
import json
from time import sleep


class Tradingview():

    URL = 'https://scanner.tradingview.com/crypto/scan'

    @staticmethod
    def get_main_headers():
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
    def get_tech_headers():
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "1261",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "scanner.tradingview.com",
            "Origin": "https://ru.tradingview.com",
            "Referer": "https://ru.tradingview.com/symbols/BCHUSD/technicals/",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    def api_query(self, data, headers):
        req = request(
            'post',
            url=Tradingview.URL,
            data=data,
            headers=headers)
        try:
            result = req.json()
        except BaseException:
            result = None
        finally:
            return result

    def get_tickers_json(self):
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
        headers = Tradingview.get_main_headers()
        return self.api_query(data, headers)

    def get_tech_json(self, ticker):
        filters_ = {
            "symbols": {
                "tickers": [],
                "query": {
                    "types": []}},
            "columns": [
                "Recommend.Other",
                "Recommend.All",
                "Recommend.MA",
                "RSI",
                "RSI[1]",
                "Stoch.K",
                "Stoch.D",
                "Stoch.K[1]",
                "Stoch.D[1]",
                "CCI20",
                "CCI20[1]",
                "ADX",
                "ADX+DI",
                "ADX-DI",
                "ADX+DI[1]",
                "ADX-DI[1]",
                "AO",
                "AO[1]",
                "Mom",
                "Mom[1]",
                "MACD.macd",
                "MACD.signal",
                "Rec.Stoch.RSI",
                "Stoch.RSI.K",
                "Rec.WR",
                "W.R",
                "Rec.BBPower",
                "BBPower",
                "Rec.UO",
                "UO",
                "EMA10",
                "close",
                "SMA10",
                "EMA20",
                "SMA20",
                "EMA30",
                "SMA30",
                "EMA50",
                "SMA50",
                "EMA100",
                "SMA100",
                "EMA200",
                "SMA200",
                "Rec.Ichimoku",
                "Ichimoku.BLine",
                "Rec.VWMA",
                "VWMA",
                "Rec.HullMA9",
                "HullMA9",
                "Pivot.M.Classic.S3",
                "Pivot.M.Classic.S2",
                "Pivot.M.Classic.S1",
                "Pivot.M.Classic.Middle",
                "Pivot.M.Classic.R1",
                "Pivot.M.Classic.R2",
                "Pivot.M.Classic.R3",
                "Pivot.M.Fibonacci.S3",
                "Pivot.M.Fibonacci.S2",
                "Pivot.M.Fibonacci.S1",
                "Pivot.M.Fibonacci.Middle",
                "Pivot.M.Fibonacci.R1",
                "Pivot.M.Fibonacci.R2",
                "Pivot.M.Fibonacci.R3",
                "Pivot.M.Camarilla.S3",
                "Pivot.M.Camarilla.S2",
                "Pivot.M.Camarilla.S1",
                "Pivot.M.Camarilla.Middle",
                "Pivot.M.Camarilla.R1",
                "Pivot.M.Camarilla.R2",
                "Pivot.M.Camarilla.R3",
                "Pivot.M.Woodie.S3",
                "Pivot.M.Woodie.S2",
                "Pivot.M.Woodie.S1",
                "Pivot.M.Woodie.Middle",
                "Pivot.M.Woodie.R1",
                "Pivot.M.Woodie.R2",
                "Pivot.M.Woodie.R3",
                "Pivot.M.Demark.S1",
                "Pivot.M.Demark.Middle",
                "Pivot.M.Demark.R1"]}
        filters_['symbols']['tickers'] = [ticker]
        data = json.dumps(filters_)
        headers = Tradingview.get_tech_headers()
        return self.api_query(data, headers)

    def get_data_Json(self):
        tickers = self.get_tickers_json()
        if tickers is None:
            return None
        data = tickers['data']
        len_ = len(data)
        for idx, row in enumerate(data):
            tickers = row['s']
            print(f'get tech info for {tickers:25} - {(idx+1):5}/{len_}')
            row_tech = self.get_tech_json(row['s'])
            if row_tech is None:
                print(f'ERROR get tech info for {tickers:25}')
                continue
            row_tech = row_tech['data'][0]['d']
            data[idx].update({'tech': row_tech})
            sleep(self.sleep)
        return data

    def __init__(self, sleep_time=0.1):
        self.sleep = sleep_time


if __name__ == '__main__':
    result = Tradingview().get_data_Json()
