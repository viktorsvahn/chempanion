#!/usr/bin/python

import argparse

from cmp.vscan.main import main as vscan_main


description = """
CLI for generating volume scans of ASE compliant atomic/molecular structures.
The generated structures have no force and energy labels but the the header in 
input xyz-files is preserved.

"""
#Omitted output (-o) will always result in a dry-run.


def register_subcommand(subparsers):
    parser = subparsers.add_parser(
        'vscan',
        help='CLI for creating volume-scans of periodic molecular structures.',
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    vscan_group = parser.add_argument_group('volume-scan')
    parser.add_argument(
        'mode',
        help='atomic or moleculecular centre of mass',
        choices=['a','m'],
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
    vscan_group.add_argument(
        '-i',
        metavar='INDEX',
        dest='index',
        default=':',
        type=str,
        required=False,
        help='structure index',
    )
    vscan_group.add_argument(
        '--min',
        metavar='MIN_SCALE',
        default=0.95,
        type=float,
        required=False,
        help='minimum cell scale factor',
    )
    vscan_group.add_argument(
        '--max',
        metavar='MAX_SCALE',
        default=1.05,
        type=float,
        required=False,
        help='maximum cell scale factor',
    )
    vscan_group.add_argument(
        '-n', 
        metavar='NUM_POINTS',
        dest='num_points',
        default=10,
        type=int,
        required=False,
        help='number of cell volumes',
    )
    parser.set_defaults(func=vscan_main)