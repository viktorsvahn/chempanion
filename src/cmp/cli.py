import argparse
from importlib.metadata import version

from cmp.vscan.cli import register_subcommand as register_vscan
from cmp.mdeq.cli import register_subcommand as register_mdeq
from cmp.db.cli import register_subcommand as register_db

version_help = f'\
chempanion ver. {version("chempanion")}'

def main():
    parser = argparse.ArgumentParser(
        prog="chempanion",
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
