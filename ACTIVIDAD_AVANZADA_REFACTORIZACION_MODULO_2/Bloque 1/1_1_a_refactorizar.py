import time

cache = {}
hits = 0
misses = 0

def get_data(key, ttl=300):
    global hits, misses
    if key in cache:
        if time.time() - cache[key]['ts'] < ttl:
            hits += 1
            return cache[key]['data']
        else:
            del cache[key]
    misses += 1
    data = fetch_from_db(key)  # pyright: ignore[reportUndefinedVariable] # función externa
    cache[key] = {'data': data, 'ts': time.time()}
    return data

def get_stats():
    return f'Hits: {hits}, Misses: {misses}, Ratio: {hits/(hits+misses)}'