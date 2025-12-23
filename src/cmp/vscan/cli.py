#!/usr/bin/python

import argparse

from cmp.vscan.main import main as vscan_main


description = """
asdasdsdasd
"""

example = """dadsadasds
"""

epilog = """Run:
> vscan 
"""


# 80-23=57 spaces wide


input_help = """dasda
"""

header_help = """dasda
"""


def register_subcommand(subparsers):
    parser = subparsers.add_parser(
        'vscan',
        help='pls',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'mode',
        help='atoms (a) or molecules (m)',
    )
    parser.add_argument(
        'input',
        help=input_help,
    )
    parser.add_argument(
        '--min',
        default=0.95,
        type=float,
        required=False,
    )
    parser.add_argument(
        '--max',
        default=1.05,
        type=float,
        required=False,
    )
    parser.add_argument(
        '-n', '--num_points',
        default=20,
        type=int,
        required=False,
    )
    parser.add_argument(
        '--output', '-o',
        default=None,
    )
    parser.set_defaults(func=vscan_main)