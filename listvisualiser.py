import sys
import pkgutil
import importlib
from random import shuffle
from arrayplot import ArrayPlot

DEFAULT_DIR = "algorithms"

def get_algorithms():
    for _, package, _ in pkgutil.iter_modules([DEFAULT_DIR]):
        module_name = '{}.{}'.format(DEFAULT_DIR, package)
        module = importlib.import_module(module_name)
        if hasattr(module, 'sort'):
            yield module.sort

def main():
    # n = 64 if len(sys.argv == 2) else int(sys.argv[1])
    n = 64
    items = list(range(1, n + 1))
    shuffle(items)

    for sort_func in get_algorithms():
        print(sort_func)
        


if __name__ == '__main__':
    main()