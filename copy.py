import os
import pathlib
import shutil
import config
import misc

def get_parser(sub_parser,parent_parsers):
    parser = sub_parser.add_parser(
        'copy',
        help="copies a file to the directory",
        aliases=['cp'],
        parents=parent_parsers
        )
    parser.add_argument(
        'source',
        action="store"
        )
    parser.add_argument(
        'destination',
        action="store",
        nargs='?',
        default=None
        )

    parser.set_defaults(func=copy)

    return parser

def copy(args):
    name, extension = os.path.splitext(os.path.basename(args.source))
    fullfilepath = ""
    if args.destination is None:
        fullfilepath = misc.generate_filename(name, extension=extension)
    else:
        fullfilepath = misc.generate_filename(args.destination, extension=extension)

    path = pathlib.Path(fullfilepath)
    if path.exists():
        print("File already exists")
        return

    shutil.copyfile(args.source, fullfilepath)




