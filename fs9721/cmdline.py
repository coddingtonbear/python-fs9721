from __future__ import print_function

import base64
import json

from measurement.base import MeasureBase
import argparse
import six

from .client import Client


def main():
    parser = argparse.ArgumentParser(
        description='Read values from your connected multimeter'
    )
    parser.add_argument('port', nargs=1, type=six.text_type)
    parser.add_argument(
        '--timeout', '-t', type=float, dest='timeout', default=3.0
    )
    parser.add_argument(
        '--retries', '-r', type=int, dest='retries', default=3
    )
    parser.add_argument(
        '--raise', '-f', default=False, action='store_true', dest='fail',
        help=(
            'Raise exceptions when errors are encountered while '
            'gathering measurements.'
        )
    )
    parser.add_argument(
        '--show-null', '-n', default=False, action='store_true', dest='null',
        help=(
            'Display null measurements.'
        )
    )
    parser.add_argument(
        '--json', '-j', default=False, action='store_true', dest='json',
    )
    args = parser.parse_args()

    dmm = Client(port=args.port[0], retries=args.retries, timeout=args.timeout)

    while True:
        try:
            response = dmm.read()
            val = response.getMeasurement()
            if val is not None or args.null:
                if args.json:
                    if isinstance(val, MeasureBase):
                        measurement = {
                            'text': str(val),
                            'unit': val.unit,
                            'value': val.value,
                            'measure': val.__class__.__name__
                        }
                    else:
                        measurement = {
                            'value': val,
                        }
                    print(
                        json.dumps(
                            {
                                'raw_value': response.rawVal,
                                'flags': response.flags,
                                'raw_bytes': (
                                    base64.b64encode(response.rawBytes)
                                ),
                                'scale_flags': response.scaleFlags,
                                'measurement_flags': response.measurementFlags,
                                'reserved_flags': response.reservedFlags,
                                'measurement': measurement,
                            }
                        )
                    )
                else:
                    print(val)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            if args.fail:
                raise

# main hook
if __name__ == "__main__":
    main()
