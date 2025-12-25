#!/usr/bin/python

import argparse
from importlib.metadata import version

from cmp.db.main import main as db_main


description = """
CLI for managing xyz-format databases, such as adding static handles and random 
sampling of structures.
"""

example = """dadsadasds
"""



# 80-23=57 spaces wide

input_help = """dasda
"""

header_help = """dasda
"""


def register_subcommand(subparsers):
    parser = subparsers.add_parser(
        'db',
        help='CLI for handling of xyz-format databases',
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'mode',
    )
    parser.add_argument(
        'input',
        help='input filename',
    )
    parser.add_argument(
        '-n',
        dest='n_samples',
        type=str,
        default=None,
        help='number of samples to draw (a number or a fraction)',
    )
    parser.add_argument(
        '--seed', '-s',
        type=int,
        default=None,
    )
    parser.add_argument(
        '--output', '-o',
        default=None,
    )
    parser.set_defaults(func=db_main)
