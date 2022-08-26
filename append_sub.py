from pathlib import Path
import toml

config = Path('config.toml')

with open(config, 'r', encoding='utf-8') as f:
    t = toml.load(f)

print(t)
print('Backup ^')

if 'reddit' not in t or 'subscriptions' not in t['reddit']:
    raise Exception(f'Invalid config file at {config}')

if not (sub := input('Subreddit name: ')):
    raise Exception('Invalid subreddit name')

t['reddit']['subscriptions'].append(sub)
t['reddit']['subscriptions'].sort()

with open(config, 'w', encoding='utf-8') as f:
    toml.dump(t, f)
