import argparse
import shutil
import sys
import os
import actions


def do_view(args):
    if args.html:
        args.pdf = False

    file = actions.find(args.search_string,n=args.n)
    if args.pdf:
        actions.view(file)

def do_create(args):
    filename = actions.create(args.name)
    if filename != None:
        print(filename)
        actions.edit(filename)

def do_find(args):
    filename = actions.find(args.search_string,n=args.n)
    if filename != None:
        print(filename)

def do_find_all(args):
    filename = actions.find(args.search_string,otherSearchPaths=True,n=args.n)
    if filename != None:
        print(filename)

def do_edit(args):
    file = actions.find(args.search_string, filterMarkdown=True,n=args.n)
    actions.edit(file)

def do_copy(args):
    name,extension = os.path.splitext(os.path.basename(args.source))
    fullfilepath = ""
    if args.destination == None:
        fullfilepath = actions.generateFilename(name,extension=extension)
    else:
        fullfilepath = actions.generateFilename(args.destination,extension=extension)
    shutil.copyfile(args.source, fullfilepath)

def do_move(args):
    name,extension = os.path.splitext(os.path.basename(args.source))
    fullfilepath = ""
    if args.destination == None:
        fullfilepath = actions.generateFilename(name,extension=extension)
    else:
        fullfilepath = actions.generateFilename(args.destination,extension=extension)
    shutil.move(args.source, fullfilepath)

def do_grep(args):
    output = actions.grep(args.search_string)
    for o in output:
        print(o)



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

    parent_config_parser = argparse.ArgumentParser(add_help=False)
    parent_config_parser.add_argument(
            '--config',
            action='store',
            default=None
            )

    parent_search_parser = argparse.ArgumentParser(add_help=False)
    parent_search_parser.add_argument(
            'search_string',
            action='store',
            help='the string to search for'
            )
    parent_search_parser.add_argument(
            'n',
            nargs='?',
            type=int,
            action='store',
            help='use the n-th item found',
            default=None
            )

    parser = argparse.ArgumentParser(parents=[parent_config_parser])
    parser_subparsers = parser.add_subparsers()


    parser_view = parser_subparsers.add_parser(
            'view',
            help="views a file found by fuzzy search",
            aliases=['v'],
            parents=[parent_config_parser,parent_search_parser]
            )

    parser_view.set_defaults(func=do_view)

    group_view = parser_view.add_mutually_exclusive_group()
    group_view.add_argument(
            '--html',
            action="store_true",
            help="produces a HTML file and views it in the browser",
            default=False
            )
    group_view.add_argument(
            '--pdf',
            action="store_true",
            help="produces a PDF file and views it in mupdf (default)",
            default=True
            )

    parser_create = parser_subparsers.add_parser(
            'create',
            help="creates a file and opens it for edit",
            aliases=['c','cr'],
            parents=[parent_config_parser]
            )
    parser_create.set_defaults(func=do_create)
    parser_create.add_argument('name',action="store")

    parser_edit = parser_subparsers.add_parser(
            'edit',
            help="opens a file for edit given by a fuzzy search",
            aliases=['e'],
            parents=[parent_config_parser,parent_search_parser]
            )
    parser_edit.set_defaults(func=do_edit)

    parser_find = parser_subparsers.add_parser(
            'find',
            help="finds a file using fuzzy search on the file name",
            aliases=['f'],
            parents=[parent_config_parser,parent_search_parser]
            )
    parser_find.set_defaults(func=do_find)

    parser_find_all = parser_subparsers.add_parser(
            'findall',
            help="finds a file using fuzzy search on the file name including the searchpaths",
            aliases=['fa'],
            parents=[parent_config_parser,parent_search_parser]
            )
    parser_find_all.set_defaults(func=do_find_all)

    parser_grep = parser_subparsers.add_parser(
            'grep',
            help="greps files",
            aliases=['g'],
            parents=[parent_config_parser,parent_search_parser]
            )
    parser_grep.set_defaults(func=do_grep)

    parser_copy = parser_subparsers.add_parser(
            'copy',
            help="copys a file to the directory",
            aliases=['cp'],
            parents=[parent_config_parser]
            )
    parser_copy.set_defaults(func=do_copy)
    parser_copy.add_argument('source',action="store")
    parser_copy.add_argument('destination',action="store",nargs='?',default=None)

    parser_move = parser_subparsers.add_parser(
            'move',
            help="moves a file to the directory",
            aliases=['mv'],
            parents=[parent_config_parser]
            )
    parser_move.set_defaults(func=do_move)
    parser_move.add_argument('source',action="store")
    parser_move.add_argument('destination',action="store",nargs='?',default=None)

    parser.set_default_subparser('view')
    return parser.parse_args()

def callAction(parsed_args):
    if hasattr(parsed_args, 'func'):
        parsed_args.func(parsed_args)

