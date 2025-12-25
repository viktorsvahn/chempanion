#!/usr/bin/python

import argparse

from cmp.mdeq.main import main as mdeq_main


description = """
CLI for equilibrating ASE compliant atomic/molecular structures intended for mol-
ecular dynamics simulations. Constant temperature simluations are based on the
Langevin thermostat and constant temperature + constant pressure simulations use
the Berendsen thermostat/barostat.

NOTE: The Berendsen thermostat/barostat should not be used for production MD and, 
by extentsion, neither should this package.
"""


def register_subcommand(subparsers):
    parser = subparsers.add_parser(
        'mdeq',
        help='CLI for MD equilibration (NVE, NVT and NPT)',
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    thermo_group = parser.add_argument_group('thermodynamic settings')
    md_group = parser.add_argument_group('MD options')
    nvt_group = parser.add_argument_group('Langevin options (NVT)')
    npt_group = parser.add_argument_group('Berendsen options (NPT)')
    
    parser.add_argument(
        'ensemble',
        help='select ensemble',
        choices=['nve','nvt','npt'],
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
    md_group.add_argument(
        '-n',
        metavar='STEPS',
        dest='steps',
        type=int,
        required=True,
        help='number of time steps',
    )
    md_group.add_argument(
        '-dt',
        metavar='TIME_STEP',
        type=float,
        default=1,
        required=False,
        help='simulation time step',
    )
    md_group.add_argument(
        '-d', 
        dest='dump_interval',
        default=10,
        type=int,
        required=False,
        help='stdout frequency',
    )
    md_group.add_argument(
        '--vscale',
        metavar='VSCALE',
        type=float,
        default=None,
        required=False,
        help='manually scale cell volume',
    )
    thermo_group.add_argument(
        '--temperature',
        metavar='TEMP',
        type=float,
        required=True,
        help='set initial/thermostat temperature',
    )
    thermo_group.add_argument(
        '--pressure',
        metavar='PRES',
        type=float,
        default=1.0,
        required=False,
        help='barostat pressure',
    )
    thermo_group.add_argument(
        '--density',
        metavar='DENS',
        type=float,
        default=None,
        help='scales cell volume to target density',
    )
    nvt_group.add_argument(
        '--friction',
        type=float,
        default=0.002,
        required=False,
        help='thermostat friction parameter',
    )
    npt_group.add_argument(
        '--taut',
        metavar='TAU_T',
        type=float,
        default=0.5,
        required=False,
        help='thermostat relaxation time',
    )
    npt_group.add_argument(
        '--taup',
        metavar='TAU_P',
        type=float,
        default=1,
        required=False,
        help='barostat relaxation time',
    )
    parser.set_defaults(func=mdeq_main)
