import subprocess
import find
import config

def get_parser(sub_parser,parent_parsers):
    parser = sub_parser.add_parser(
        'edit',
        help="opens a file for editing",
        aliases=['e'],
        parents=parent_parsers
        )

    parser.set_defaults(func=edit)

    return parser

def edit(args):
    file = find.find(args)
    if file is None:
        return
    subprocess.call([config.Config.getPrograms()['editor'], file])
