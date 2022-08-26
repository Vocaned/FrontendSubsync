from pathlib import Path
import json
import toml
import requests

def str_js(v) -> str:
    """Stringify an object with js[on] compatible booleans"""
    if isinstance(v, bool):
        return str(v).lower()
    return str(v)

def ensure_output():
    Path('output', 'cache').mkdir(parents=True, exist_ok=True)

def cache_subs():
    '''Get subreddit ID and icon from reddit api, and save to cache'''
    with open('config.toml', 'r', encoding='utf-8') as f:
        t = toml.load(f)
        subs = t['reddit']['subscriptions']

    sub_cache = Path('output', 'cache', 'sub_id.json')

    entries = {}
    if sub_cache.exists():
        with open(sub_cache, 'r', encoding='utf-8') as f:
            entries = json.load(f)

    try:
        for sub in subs:
            if sub.lower() in entries:
                continue
            print(f'Getting info: {sub}')

            about = requests.get(f'https://reddit.com/r/{sub}/about.json', headers={'User-Agent': 'Infinity sublist gen'}).json()
            if not 'data' in about or 'error' in about:
                raise Exception(f'{sub}: {about}')
            about = about['data']
            entries[sub.lower()] = {
                'name': about['display_name'],
                'id': about['name'],
                'iconUrl': about['community_icon']
            }
    finally:
        with open(sub_cache, 'w', encoding='utf-8') as f:
            json.dump(entries, f)
