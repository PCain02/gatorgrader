"""Check that a repository has the required number of commits."""

import argparse

from gator import checkers


def get_parser():
    """Get a parser for the arguments provided on the command-line."""
    # create the parser with the default help formatter
    # use a new description since this is a stand-alone check
    parser = argparse.ArgumentParser(
        prog="CountCommits",
        description="Check Provided by GatorGrader: CountCommits",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required Named Checker Arguments {{{

    required_group = parser.add_argument_group("required check arguments")

    # COUNT: the number of commits
    # REQUIRED? Yes
    required_group.add_argument(
        "--count", type=int, help="minimum number of git commits", required=True
    )

    # }}}

    # Optional Named Checker Arguments {{{

    optional_group = parser.add_argument_group("optional check arguments")

    # EXACT: perform exact checking for commit counts (i.e,. "==" instead of ">=")
    # REQUIRED? No
    optional_group.add_argument(
        "--exact", help="equals instead of a minimum number", action="store_true"
    )

    # }}}
    return parser


def parse(args, parser=None):
    """Use the parser on the provided arguments."""
    checkers.parse(get_parser, args, parser)
