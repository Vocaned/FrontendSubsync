import toml

from utils import ensure_output, cache_subs, str_js

def main():
    with open('config.toml', 'r', encoding='utf-8') as f:
        t = toml.load(f)
        subs = t['reddit']['subscriptions']

    opts = t['teddit']

    opts['subbed_subreddits'] = f'j:["{",".join(subs)}"]'

    cookies = ''

    for k,v in opts.items():
        cookies += f"document.cookie = '{str_js(k)}={str_js(v)};expires=Fri, 31 Dec 9999 23:59:59 UTC;path=/;SameSite=Lax;'\n"

    with open('output/teddit_cookies.js', 'w', encoding='utf-8') as f:
        f.write(cookies)

if __name__ == '__main__':
    ensure_output()
    cache_subs()
    main()
    print('Cookies written to teddit_cookies.js. Copy the script contents to your developer tools console.')
