# encoding=utf-8

import getopt
import sys


def main(argv):
    try:
        options, args = getopt.getopt(argv, "hn:m:", ["help", "start=", "end="])
    except getopt.GetoptError as e:
        print('args', e)
        sys.exit()
    print('args', options[0][1])
    for value in range(int(options[0][1]), int(options[1][1])):
        if value == '%':
            return
        print(str(value), end=',')


if __name__ == '__main__':
    main(sys.argv[1:])
