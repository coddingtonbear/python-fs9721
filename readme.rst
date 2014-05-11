Easily gather measurements from your multimeter using the
Fortune Semiconductors FS9721_LP3 protocol.

Installation
------------

Install from Github directly::
    
    git clone https://github.com/coddingtonbear/python-fs9721.git
    cd python-fs9721
    python setup.py install

or, install from PyPI using ``pip``::

    pip install fs9721

Use as a Library
----------------

Create the client you'll use for gathering measurements first.  Using
the path to the serial device, create an instance of ``fs9721.Client``::

    from fs9721 import Client

    my_multimeter = Client('/dev/tty.usbserial')

Then, you can gather measurements from your multimeter using::

    print(my_multimeter.getMeasurement())

Command-Line Use
----------------

For basic use, just run::

    fs9721 /path/to/serial/port

For example, on my computer the device is connected via the serial port
at ``/dev/tty.usbserial``, for me to gather measurements directly from
the multimeter, I would run::

    fs9721 /dev/tty.usbserial

Command-Line Options
~~~~~~~~~~~~~~~~~~~~

* ``--timeout=3.0``: Number of seconds to wait before timing out when
  communicating with the multimeter.  Default: 3 seconds.
* ``--retries=COUNT``: Number of times to retry after failing to communicate
  with the multimeter.
* ``--format=FORMAT``: One of ``json``, ``csv``, or ``text`` (defaulting to
  ``text``) corresponding with the format in which you would like the data
  formatted.
* ``--file=PATH``: Rather than writing the output to the console via stdout,
  write file to the specified file.
* ``--raise``: Due to the relative commonness of errors in communication with
  the multimeter, communication errors are suppressed by default.  Use this
  option to raise exceptions for errors that occur.
* ``-show-null``: Null measurements from the multimeter are suppressed by
  default, use this option to display null measurements when they are returned.
* ``-separator``: Separator to use for CSV formatter.  Defaults to ','','.

Command-Line Examples
~~~~~~~~~~~~~~~~~~~~~

The following examples all assume that your device is connected to
``/dev/mydevice``.

* Write output to console in the simple text format::

  fs9721 /dev/mydevice

* Write output to console in CSV (comma-separated values) format::

  fs9721 --format=csv /dev/mydevice

* Write output to the console in tab-delimited format::

  fs9721 --format=csv --separator=$'\t' /dev/mydevice

* Write output to file at ``/tmp/myoutput.tdv.csv`` in tab-delimited format::

  fs9721 --format=csv --file=/tmp/myoutput.tdv.csv --separator=$'\t' /dev/mydevice

* Write output to console in JSON format::

  fs9721 --format=json /dev/mydevice

.. note::

   If you aren't familiar with the ``$'\t'`` notation: when preceding a string
   with a dollar sign symbol, you are instructing Bash (assuming you are using
   Bash as your shell) to convert the basckslash notation into the actual
   character the backslash notation refers to.  For more information, please consult
   `this article on Stack Overflow <http://stackoverflow.com/questions/14251307/can-i-pass-t-to-python-from-the-command-line>`_.

Does this support my multimeter?
--------------------------------

This library should support any multimeter using the
Fortune Semiconductors FS9721_LP3 chip.
Common multimeters using this chip are often low-end and include the following:

* TekPower TP4000ZC
* UNI-T_UT60E
* V&A V18b
* Voltcraft VC-820 and VC-840

If your multimeter is not on the above list, do not despair!
This specific IC is very common, and it may very use this chip.
Sigrok has a nice reference of which chips various multimeters use;
`search for your multimeter on their wiki <http://sigrok.org/wiki/Main_Page>`_
to see if yours also uses this DMM IC.
