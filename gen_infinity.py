import json
import pyminizip
import os
import toml

from utils import ensure_output, cache_subs

def main():
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
            'name': sub_info[sub]['name'],
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
    cache_subs()
    main()
