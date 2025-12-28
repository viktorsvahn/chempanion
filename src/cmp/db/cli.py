#!/usr/bin/python

import argparse
from importlib.metadata import version

from cmp.db.main import main as db_main


description = """
CLI for managing xyz-format databases, such as adding static handles and random 
sampling of structures.

Omitted output (-o) will always result in a dry-run.
"""


def register_subcommand(subparsers):
    parser = subparsers.add_parser(
        'db',
        help='CLI for handling of xyz-format databases',
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    select_group = parser.add_argument_group('selection')
    rand_group = parser.add_argument_group('random sampling')

    parser.add_argument(
        'mode',
        help='database action',
        choices=['sample'],
    )
    parser.add_argument(
        'input',
        help='input filename',
    )
    parser.add_argument(
        '-o',
        dest='output',
        default=None,
        help='output filename',
    )
    select_group.add_argument(
        '--info',
        nargs=2,
        metavar=('HANDLE','VALUE'),
        dest='handle',
        type=str,
        default=None,
        help='select structures where info-HANDLE matches VALUE (wildcards supported)',
    )
    rand_group.add_argument(
        '-n',
        dest='n_samples',
        type=str,
        default=None,
        help='number of samples to draw (a number or a fraction)',
    )
    rand_group.add_argument(
        '--seed',
        help='numpy random seed (default None)',
        type=int,
        default=None,
    )
    parser.set_defaults(func=db_main)