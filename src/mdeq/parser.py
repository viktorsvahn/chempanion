#!/usr/bin/python

from importlib.metadata import version
import argparse

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

version_help = f'\
treerun ver. {version("treerun")}'


input_help = """dasda
"""

header_help = """dasda
"""


def argument_parser():
    parser = argparse.ArgumentParser(
        prog='mdeq',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--version', action='version',
        version=version_help,
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
    )
    parser.add_argument(
        '--scale',
        type=float,
        default=1.0,
    )
    parser.add_argument(
        '--friction',
        type=float,
        default=0.002,
    )
    parser.add_argument(
        '--output', '-o',
        default=None,
    )
    parser.add_argument(
        '--header', type=int, nargs='+',
        help=input_help,
    )
    return parser.parse_args()
