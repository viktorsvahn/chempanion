#!/usr/bin/python

import argparse

from ccm.mdeq.main import main as mdeq_main


description = """
asdasdsdasd
"""

example = """dadsadasds
"""

epilog = """Run:
> mdeq --example
to see an example tree structure with its associated input file.
"""


# 80-23=57 spaces wide


input_help = """dasda
"""

header_help = """dasda
"""


def register_subcommand(subparsers):
    parser = subparsers.add_parser(
        'mdeq',
        help='pls',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'ensemble',
    )
    parser.add_argument(
        'input',
        help=input_help,
    )
    parser.add_argument(
        '--steps',
        type=int,
        required=True,
    )
    parser.add_argument(
        '--temperature',
        '--temp',
        type=float,
        required=True,
    )
    parser.add_argument(
        '-dt',
        type=float,
        default=1,
        required=False,
    )
    parser.add_argument(
        '--pressure',
        type=float,
        default=1.0,
        required=False,
    )
    parser.add_argument(
        '--friction',
        type=float,
        default=0.002,
        required=False,
    )
    parser.add_argument(
        '--taut',
        type=float,
        default=0.5,
        required=False,
    )
    parser.add_argument(
        '--taup',
        type=float,
        default=1,
        required=False,
    )
    parser.add_argument(
        '--scale',
        type=float,
        default=None,
        required=False,
    )
    parser.add_argument(
        '--density',
        type=float,
        default=None,
    )
    parser.add_argument(
        '-d', '--dump_interval',
        default=10,
        type=int,
        required=False,
    )
    parser.add_argument(
        '--output', '-o',
        default=None,
    )
    parser.add_argument(
        '--header', type=int, nargs='+',
        help=input_help,
    )
    parser.set_defaults(func=mdeq_main)
