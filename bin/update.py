import sh
import config

def get_parser(sub_parser,parent_parsers):
    parser = sub_parser.add_parser(
        'update',
        help="updates the directory for the notes using git",
        aliases=['u'],
        parents=parent_parsers
        )

    parser.set_defaults(func=update)

    return parser

def update(args):
    try:
        val = sh.git(
            "-C",
            config.Config.getPath(),
            "pull",
            "origin",
            "master")
        print(val)
    except sh.ErrorReturnCode:
        print(val)
        return
    try:
        val = sh.git(
            "-C",
            config.Config.getPath(),
            "add",
            "-A")
        print(val)
    except sh.ErrorReturnCode:
        print(val)
        return
    try:
        val = sh.git(
            "-C",
            config.Config.getPath(),
            "commit",
            "-a",
            "-m",
            "update")
        print(val)
    except sh.ErrorReturnCode:
        print(val)
        return
    try:
        val = sh.git(
            "-C",
            config.Config.getPath(),
            "push",
            "origin",
            "master")
        print(val)
    except sh.ErrorReturnCode:
        print(val)
        return
