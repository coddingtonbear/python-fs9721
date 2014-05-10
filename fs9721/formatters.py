import datetime
import base64
from json import dumps as json_dumps

from measurement.base import MeasureBase
import six


registered_formatters = {}


def register_formatter(fn):
    global registered_formatters
    registered_formatters[fn.__name__] = fn
    return fn


@register_formatter
def json(idx, reading, val):
    if not val:
        return ''
    if isinstance(val, MeasureBase):
        measurement_dict = {
            'measure': val.__class__.__name__,
            'text': str(val),
            'unit': val.unit,
            'value': val.value,
            'standardized_value': val.standard,
            'standardized_unit': val.STANDARD_UNIT
        }
    else:
        measurement_dict = {
            'value': val,
        }
    return [
        json_dumps(
            {
                'index': idx,
                'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
                'raw_value': reading.rawVal,
                'flags': reading.flags,
                'raw_bytes': (
                    base64.b64encode(reading.rawBytes)
                ),
                'scale_flags': reading.scaleFlags,
                'measurement_flags': reading.measurementFlags,
                'reserved_flags': reading.reservedFlags,
                'measurement': measurement_dict,
            }
        )
    ]


@register_formatter
def csv(idx, reading, val):
    lines = []
    if idx == 0:
        lines.append(
            ','.join([
                'Index',
                'Timestamp',
                'Value',
                'Unit',
                'Standardized Value',
                'Standardized Unit',
                'Measure',
                'Human-Readable',
                'Raw Value',
                'Base64 Bytes',
                'Reading Flags',
                'Scale Flags',
                'Measurement Flags',
                'Reserved Flags',
            ])
        )
    if not val:
        return ''
    cols = [
        idx,
        datetime.datetime.utcnow().isoformat() + 'Z',
    ]
    if isinstance(val, MeasureBase):
        cols.extend(
            [
                val.value,
                val.unit,
                val.standard,
                val.STANDARD_UNIT,
                val.__class__.__name__,
                str(val)
            ]
        )
    else:
        cols.extend(
            [
                val,
                '',
                '',
                '',
                '',
                '',
            ]
        )
    cols.extend(
        [
            reading.rawVal,
            base64.b64encode(reading.rawBytes),
            ';'.join(reading.flags),
            ';'.join(reading.scaleFlags),
            ';'.join(reading.measurementFlags),
            ';'.join(reading.reservedFlags),
        ]
    )
    lines.append(','.join([six.text_type(v).encode('utf-8') for v in cols]))
    return lines


@register_formatter
def text(idx, reading, val):
    return [val]
