import json
import pyminizip
import requests
import os
import toml

from utils import ensure_output

def stage1():
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
            if sub in entries:
                continue
            print(f'Getting info: {sub}')

            about = requests.get(f'https://reddit.com/r/{sub}/about.json', headers={'User-Agent': 'Infinity sublist gen'}).json()
            if 'data' not in about:
                Exception(about)
            about = about['data']
            entries[sub] = {
                'id': about['name'],
                'iconUrl': about['community_icon']
            }
    finally:
        with open('output/cache/sub_id.json', 'w', encoding='utf-8') as f:
            json.dump(entries, f)

def stage2():
    '''Turn sub data into an Infinity backup zip'''
    with open('config.toml', 'r', encoding='utf-8') as f:
        t = toml.load(f)
        subs = t['reddit']['subscriptions']

    with open('output/cache/sub_id.json', 'r', encoding='utf-8') as f:
        sub_info = json.load(f)

    entries = []

    for sub in subs:
        entries.append({
            'favorite': False,
            'username': '-',
            'name': sub,
            'id': sub_info[sub]['id'],
            'iconUrl': sub_info[sub]['iconUrl']
        })

    with open('output/cache/anonymous_subscribed_subreddits.json', 'w', encoding='utf-8') as f:
        json.dump(entries, f)

    pyminizip.compress('output/cache/anonymous_subscribed_subreddits.json', '5.2.0/database/', 'output/infinity_backup.zip', '123321', 0)

    os.remove('output/cache/anonymous_subscribed_subreddits.json')

    print('Subscriptions written to output/infinity_backup.zip. Import the file in Advanced > Restore Settings in Infinity')

if __name__ == '__main__':
    ensure_output()
    stage1()
    stage2()
