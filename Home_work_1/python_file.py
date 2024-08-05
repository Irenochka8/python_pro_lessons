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
                _update_freq(cache_key)
                return deco._cache[cache_key]
            result = f(*args, **kwargs)
            if len(deco._cache) >= max_limit:
                _key_out()
            deco._cache[cache_key] = result
            deco._freq[cache_key] = 1
            deco._freq_order[1].add(cache_key)
            return result

        def _update_freq(key):
            current_freq = deco._freq[key]
            new_freq = current_freq + 1
            deco._freq[key] = new_freq
            deco._freq_order[current_freq].remove(key)
            if not deco.freq_order[current_freq]:
                del deco._freq_order[current_freq]
            if new_freq not in deco._freq_order:
                deco._freq_order[new_freq] = set()
            deco._freq_order[new_freq].add(key)
        def _key_out():
            min_freq = min(deco._freq_order.keys())
            least_used_key = deco._freq_order[min_freq].pop()
            if not deco._freq_order[min_freq]:
                del deco._freq_order[min_freq]
            del deco._cache[least_used_key]
            del deco._freq[least_used_key]

        deco._cache = OrderedDict()
        deco._freq = {}
        deco._freq_order = collections.defaultdict(set)
        deco._update_freq = _update_freq
        deco._key_out = _key_out
        return deco
    return internal

import requests
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
