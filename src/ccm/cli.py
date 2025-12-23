import argparse
from importlib.metadata import version

from ccm.vscan.cli import register_subcommand as register_vscan
from ccm.mdeq.cli import register_subcommand as register_mdeq
from ccm.db.cli import register_subcommand as register_db

version_help = f'\
treerun ver. {version("treerun")}'

def main():
    parser = argparse.ArgumentParser(
        prog="ccm",
        description="My modular CLI"
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        dest='subcommand',
        required=True,
    )
    parser.add_argument(
        '--version', action='version',
        version=version_help,
    )

    # Register commands
    register_vscan(subparsers)
    register_mdeq(subparsers)
    register_db(subparsers)

    args = parser.parse_args()
    args.func(args)
