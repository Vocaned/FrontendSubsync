import toml

from utils import ensure_output, cache_subs, str_js

def main():
    with open('config.toml', 'r', encoding='utf-8') as f:
        t = toml.load(f)
        subs = t['reddit']['subscriptions']

    opts = t['teddit']

    opts['subbed_subreddits'] = 'j:["' + '","'.join(subs) + '"]'

    cookies = ''

    for k,v in opts.items():
        k,v = (str_js(k),str_js(v))
        cookies += f"document.cookie = '{k}={v};expires=2147483647;path=/;SameSite=Strict;'\n"

    with open('output/teddit_cookies.js', 'w', encoding='utf-8') as f:
        f.write(cookies)

    print('Cookies written to teddit_cookies.js. Copy the script contents to your developer tools console.')

if __name__ == '__main__':
    ensure_output()
    cache_subs()
    main()
