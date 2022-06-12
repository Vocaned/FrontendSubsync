import os

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
