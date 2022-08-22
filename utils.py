import os
import toml
import requests
import json

def str_js(v) -> str:
    """Stringify an object with js[on] compatible booleans"""
    if isinstance(v, bool):
        return str(v).lower()
    return str(v)

def ensure_output():
    if not os.path.isdir('output'):
        if os.path.exists('output'):
            raise Exception('output already exists, but is a file instead of a directory.')
        os.mkdir('output')
        os.mkdir('output/cache')
    if not os.path.isdir('output/cache'):
        if os.path.exists('output/cache'):
            raise Exception('output/cache already exists, but is a file instead of a directory.')
        os.mkdir('output/cache')

def cache_subs():
    '''Get subreddit ID and icon from reddit api, and save to cache'''
    with open('config.toml', 'r', encoding='utf-8') as f:
        t = toml.load(f)
        subs = t['reddit']['subscriptions']

    entries = {}
    if os.path.exists('output/cache/sub_id.json'):
        with open('output/cache/sub_id.json', 'r', encoding='utf-8') as f:
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
        with open('output/cache/sub_id.json', 'w', encoding='utf-8') as f:
            json.dump(entries, f)
