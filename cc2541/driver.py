import os
import six
import sys

import argparse
import optparse

from cc2541.sensor import get_data

parser = argparse.ArgumentParser(description='BLE Robotice Driver.')
parser.add_argument('address', nargs='?', help='Address')
parser.add_argument('-r', '--repeat', action='store_true', help="Repeat", default=False)

def pp(data):

    for datum in data:
        print str(datum)

def main():

    args = parser.parse_args()
    
    bluetooth_adr = getattr(args, "address", sys.argv[1]) 

    pp(get_data({"address":bluetooth_adr}))

    if args.repeat:

        while True:
            pp(get_data({"address":bluetooth_adr}))

if __name__ == "__main__":
    main()