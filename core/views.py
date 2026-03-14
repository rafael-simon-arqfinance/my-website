import time
import threading

import yfinance as yf
from django.shortcuts import render
from django.http import JsonResponse

SECURITIES = {
    'ODF 27':  'DI1F27.SA',
    'ODF 29':  'DI1F29.SA',
    'USD/BRL': 'BRL=X',
    'BTC/USD': 'BTC-USD',
    'S&P 500': '^GSPC',
}

_cache: dict = {}
_cache_lock = threading.Lock()
CACHE_TTL = 600  # 10 minutes


def _get_cached(key, fetcher):
    with _cache_lock:
        entry = _cache.get(key)
        if entry and time.time() - entry['ts'] < CACHE_TTL:
            return entry['data']
    data = fetcher()
    with _cache_lock:
        _cache[key] = {'ts': time.time(), 'data': data}
    return data


def home(request):
    return render(request, 'core/home.html')


def api_history(request):
    def fetch():
        result = {}
        for label, ticker in SECURITIES.items():
            try:
                hist = yf.Ticker(ticker).history(period='1mo', interval='1d')
                if hist.empty:
                    result[label] = {'dates': [], 'prices': []}
                else:
                    result[label] = {
                        'dates':  hist.index.strftime('%b %d').tolist(),
                        'prices': [round(float(p), 4) for p in hist['Close'].tolist()],
                    }
            except Exception:
                result[label] = {'dates': [], 'prices': []}
        return result

    return JsonResponse(_get_cached('history', fetch))


def api_prices(request):
    def fetch():
        result = {}
        for label, ticker in SECURITIES.items():
            try:
                fi = yf.Ticker(ticker).fast_info
                price = fi.last_price
                if price is None:
                    hist = yf.Ticker(ticker).history(period='1d', interval='1m')
                    price = float(hist['Close'].iloc[-1]) if not hist.empty else None
                result[label] = round(float(price), 4) if price is not None else None
            except Exception:
                result[label] = None
        return result

    return JsonResponse(_get_cached('prices', fetch))


def page2(request):
    return render(request, 'core/page2.html')


def page3(request):
    return render(request, 'core/page3.html')
