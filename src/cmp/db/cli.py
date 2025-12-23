#!/usr/bin/python

import argparse
from importlib.metadata import version

from cmp.db.main import main as db_main


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


def register_subcommand(subparsers):
    parser = subparsers.add_parser(
        'db',
        help='pls',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'input',
        help=input_help,
    )
    parser.add_argument(
        '--output', '-o',
        default=None,
    )