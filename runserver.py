#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Authors: Max Chan, Louis Aaron
#-----------------------------------------------------------------------

import sys
import argparse
import registrar

#-----------------------------------------------------------------------

def parse_input():
    parser = argparse.ArgumentParser(
    description='The registrar application',
    allow_abbrev=False)

    parser.add_argument('port', metavar='port', type=int,
    help='the port at which the server should listen')

    return parser.parse_args()

#-----------------------------------------------------------------------

def main():

    args = parse_input()

    port = int(args.port)

    try:
        registrar.app.run(host='0.0.0.0', port=port, debug=True)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
