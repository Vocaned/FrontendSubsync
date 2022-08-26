from gen_infinity import main as infinity
from gen_teddit import main as teddit

from utils import ensure_output, cache_subs

if __name__ == '__main__':
    ensure_output()
    cache_subs()

    print('Generating Infinity backup zip')
    infinity()

    print('Generating Teddit cookies')
    teddit()

    print('Files generated to the `output` directory.')
