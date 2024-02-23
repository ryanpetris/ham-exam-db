#!/usr/bin/env python3

import sys


def dep_check_main():
    try:
        import docx
    except ImportError:
        print('python-docx module required. https://github.com/python-openxml/python-docx', file=sys.stderr)
        exit(1)

    print('All required modules installed', file=sys.stderr)


if __name__ == '__main__':
    dep_check_main()
