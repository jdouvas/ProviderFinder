#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Julia Douvas
#-----------------------------------------------------------------------

from sys import exit, stderr
import argparse
from app import app

def main():
    parser = argparse.ArgumentParser(description='Application to find a mental healthcare provider', allow_abbrev=False)
    parser.add_argument('port', type=int, metavar='port', help='the port at which the server should listen')

    try:
        args = parser.parse_args()
        app.run(port=args.port, debug=True)
    except argparse.ArgumentError:
        parser.print_help()
        exit(2)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()