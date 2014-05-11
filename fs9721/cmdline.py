from __future__ import print_function

import argparse
import six

from .client import Client
from .formatters import registered_formatters


def main():
    parser = argparse.ArgumentParser(
        description='Read values from your connected multimeter'
    )
    parser.add_argument('port', nargs=1, type=six.text_type)
    parser.add_argument(
        '--timeout', type=float, dest='timeout', default=3.0
    )
    parser.add_argument(
        '--retries', type=int, dest='retries', default=3
    )
    parser.add_argument(
        '--raise', default=False, action='store_true', dest='raise_err',
        help=(
            'Raise exceptions when errors are encountered while '
            'gathering measurements.'
        )
    )
    parser.add_argument(
        '--show-null', default=False, action='store_true', dest='null',
        help=(
            'Display null measurements.'
        )
    )
    parser.add_argument(
        '--format', '-f', default='text', dest='format', type=six.text_type
    )
    parser.add_argument(
        '--file', '-o', default=None, dest='outfile', type=six.text_type
    )
    args, extra = parser.parse_known_args()

    dmm = Client(port=args.port[0], retries=args.retries, timeout=args.timeout)

    formatter = registered_formatters[args.format]
    idx = 0
    if args.outfile:
        outfile = open(args.outfile, 'w')
    while True:
        try:
            response = dmm.read()
            val = response.getMeasurement()
            if val is not None or args.null:
                lines = formatter(idx, response, val, extra=extra)
                for line in lines:
                    if args.outfile:
                        outfile.write(line)
                        outfile.write('\n')
                    else:
                        print(line)
                if lines:
                    idx += 1
        except (KeyboardInterrupt, SystemExit):
            if args.outfile:
                outfile.close()
            raise
        except:
            if args.raise_err:
                raise
    if args.outfile:
        outfile.close()

# main hook
if __name__ == "__main__":
    main()
