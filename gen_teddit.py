import json
import toml

from utils import ensure_output

def main():
    with open('config.toml', 'r', encoding='utf-8') as f:
        t = toml.load(f)
        subs = t['reddit']['subscriptions']
        hostname = t['teddit']['instance']
        del t['teddit']['instance']

    assert not hostname.startswith('https:'), 'Instance cannot being with https://. Either use http:// or only the host'
    if not hostname.startswith('http://'):
        hostname = 'http://' + hostname

    opts = t['teddit']

    opts['subbed_subreddits'] = 'j:["' + '","'.join(subs) + '"]'

    cookies = []

    for k,v in opts.items():
        cookies.append({
            'Name raw': k,
            'Content raw': v,
            'Host raw': hostname,
            'Path raw': '/',
            'HTTP only raw': 'true',
            'Expires raw': '2147483647'
        })

    with open('output/teddit_cookies.json', 'w', encoding='utf-8') as f:
        json.dump(cookies, f)

    print('Cookies written to teddit_cookies.json. Use Cookie Quick Manager to import them to your browser.')

if __name__ == '__main__':
    ensure_output()
    main()
