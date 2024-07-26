#Task1
import collections
import functools
from collections import OrderedDict
def cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in deco._cache:
                # увеличиваем частоту доступа
                deco._freq[cache_key] += 1
                return deco._cache[cache_key]
            result = f(*args, **kwargs)
            # видаляємо якшо досягли ліміта
            if len(deco._cache) >= max_limit:
                 # ищем наименьшее по частоте использования
                 min_freq = min(deco._freq.values())
                 least_freq_keys = [key for key, freq in deco._freq.items() if freq == min_freq]
                 min_freq_key = least_freq_keys[0]
                 # и удаляем
                 del deco._cache[min_freq_key]
                 del deco._freq[min_freq_key]
            deco._cache[cache_key] = result
            deco._freq[cache_key] = 1
            return result
        deco._cache = OrderedDict()
        deco._freq = collections.defaultdict(int) #для хранения по частоте
        return deco
    return internal

@cache(max_limit=64)
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

#Task2

import tracemalloc

def memory_dec(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        snapshot_1 = tracemalloc.take_snapshot()
        result = f(*args, **kwargs)
        snapshot_2 = tracemalloc.take_snapshot()
        tracemalloc.stop()
        stats_memory = snapshot_2.compare_to(snapshot_1, 'lineno')
        print(f"use_memory:{stats_memory}")
        return result
    return wrapper

@memory_dec
def add_numb(a, b):
    return a + b
result = add_numb(1,7)
print(result)
