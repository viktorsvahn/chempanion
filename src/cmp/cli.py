import argparse
from importlib.metadata import version

from cmp.vscan.cli import register_subcommand as register_vscan
from cmp.mdeq.cli import register_subcommand as register_mdeq
from cmp.db.cli import register_subcommand as register_db

version_help = f'\
Chempanion ver. {version("chempanion")}'

description = '''\
Chempanion is a CLI for a collection of tools that are useful within the realm of
molecular simulation, such as equilibration of MD structures, generating volume-
scans, random sampling, etc.'''

def show_banner(args):
    print(r"""
   _____ _                                      _             
  / ____| |                                    (_)            
 | |    | |__   ___ _ __ ___  _ __   __ _ _ __  _  ___  _ __  
 | |    | '_ \ / _ \ '_ ` _ \| '_ \ / _` | '_ \| |/ _ \| '_ \ 
 | |____| | | |  __/ | | | | | |_) | (_| | | | | | (_) | | | |
  \_____|_| |_|\___|_| |_| |_| .__/ \__,_|_| |_|_|\___/|_| |_|
                             | |                              
                             |_|                              
    """)
    print(version_help)
    print('\nCall:\n> cmp -h\nfor further instructions on usage.')


def main():
    parser = argparse.ArgumentParser(
        prog="cmp",
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--version', action='version',
        version=version_help,
    )
    parser.set_defaults(func=show_banner)

    subparsers = parser.add_subparsers(
        title="subcommands",
        dest='subcommand',
        required=False,
    )

    # Register commands
    register_vscan(subparsers)
    register_mdeq(subparsers)
    register_db(subparsers)

    args = parser.parse_args()
    args.func(args)
