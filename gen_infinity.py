import json
from pathlib import Path
import pyminizip
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
            'name': sub_info[sub.lower()]['name'],
            'id': sub_info[sub.lower()]['id'],
            'iconUrl': sub_info[sub.lower()]['iconUrl']
        })

    temp_json = Path('output/cache/anonymous_subscribed_subreddits.json')

    with open(temp_json, 'w', encoding='utf-8') as f:
        json.dump(entries, f)

    # Infinity backup zips are password protected with the password `123321`
    # https://github.com/Docile-Alligator/Infinity-For-Reddit/blob/ddfc478e0e9f95b8630a16dd3a179bb4acfca10a/app/src/main/java/ml/docilealligator/infinityforreddit/asynctasks/RestoreSettings.java#L88
    password = '123321'
    pyminizip.compress(str(temp_json), '5.2.0/database/', 'output/infinity_backup.zip', password, 0)

    temp_json.unlink()

if __name__ == '__main__':
    ensure_output()
    cache_subs()
    main()
    print('Subscriptions written to output/infinity_backup.zip. Import the file in Advanced > Restore Settings in Infinity')
