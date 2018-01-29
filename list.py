import find
import config

def get_parser(sub_parser,parent_parsers):
    parser = sub_parser.add_parser(
        'list',
        help="lists files matching a search",
        aliases=['l'],
        parents=parent_parsers
        )

    parser.set_defaults(func=list)

    return parser

def list(args):
    file = find.find(args)
    if not file is None:
        print("0: {}".format(file))
