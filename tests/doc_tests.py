import doctest
from src import scldata as sd


def main():
    doctest.testmod(sd, verbose=True)

if __name__ == '__main__':
    main()
