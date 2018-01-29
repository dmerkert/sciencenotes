import pathlib
import datetime
import config
import misc

def get_parser(sub_parser,parent_parsers):
    parser = sub_parser.add_parser(
        "create",
        help="creates a new file in Markdown",
        aliases=['c', 'cr'],
        parents=parent_parsers
        )

    parser.set_defaults(func=create)

    parser.add_argument(
        'name',
        help="the name of the file to create, exclusive the date.",
        action="store")

    return parser

def create(args):
    fullfilepath = misc.generate_filename(args.name)
    path = pathlib.Path(fullfilepath)
    print(fullfilepath)

    if path.exists():
        print("File already exists")
        return

    pathlib.Path(fullfilepath).touch()

    with open(fullfilepath, "w") as f:
        f.write("---\n")
        f.write("author: \n")
        f.write("title: \"\"\n")
        f.write("date: {}\n".format(datetime.date.today().strftime("%Y-%m-%d")))
        f.write("subtitle: \"\"\n")
        f.write("type: \n")
        f.write("tags:\n")
        f.write("  - \n")
        f.write("---\n")

