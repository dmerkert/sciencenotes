import argparse
import shutil
import sys
import os

import config
import copy
import create
import edit
import find
import move
import update
import view
import list

def set_default_subparser(self, name, args=None):
    """default subparser selection. Call after setup, just before parse_args()
    name: is the name of the subparser to call by default
    args: if set is the argument list handed to parse_args()

    , tested with 2.7, 3.2, 3.3, 3.4
    it works with 2.6 assuming argparse is installed
    """
    subparser_found = False
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:  # global help if no subparser
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
        if not subparser_found:
            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            if args is None:
                sys.argv.insert(1, name)
            else:
                args.insert(0, name)


def parse():
    argparse.ArgumentParser.set_default_subparser = set_default_subparser

    parser_config = config.get_parser(argparse)
    parser_find = find.get_parser(argparse)

    parser = argparse.ArgumentParser(parents=[parser_config])
    parser_subparsers = parser.add_subparsers()

    parser_copy = copy.get_parser(
        parser_subparsers,
        [parser_config, parser_find]
        )

    parser_create = create.get_parser(
        parser_subparsers,
        [parser_config]
        )

    parser_edit = edit.get_parser(
        parser_subparsers,
        [parser_config, parser_find]
        )

    parser_move = move.get_parser(
        parser_subparsers,
        [parser_config, parser_find]
        )

    parser_update = update.get_parser(
        parser_subparsers,
        [parser_config]
        )

    parser_view = view.get_parser(
        parser_subparsers,
        [parser_config, parser_find]
        )

    parser_list = list.get_parser(
        parser_subparsers,
        [parser_config, parser_find]
        )


    parser.set_default_subparser('view')
    return parser.parse_args()

def callAction(parsed_args):
    if hasattr(parsed_args, 'func'):
        parsed_args.func(parsed_args)

