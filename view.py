import subprocess
import tempfile
import pypandoc
import config
import find

def get_parser(sub_parser,parent_parsers):
    parser = sub_parser.add_parser(
        "view",
        help="displays the file as pdf or html (in case of Markdown)" +
        " and in the native format, otherwise.",
        aliases=['v'],
        parents=parent_parsers
        )

    parser.set_defaults(func=view)

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--html',
        action="store_true",
        help="produces a HTML file.",
        default=False
        )
    group.add_argument(
        '--pdf',
        action="store_true",
        help="produces a PDF file.",
        default=True
        )
    return parser

def view(args):
    if args.html:
        args.pdf = False

    file = find.find(args)
    if file is None:
        return

    if file.endswith(".md"):
        with tempfile.TemporaryDirectory() as tmpdir:
            if args.pdf:
                tmpfile_name = "{}/{}".format(tmpdir, "tmp.pdf")
                pypandoc.convert_file(file, "pdf", outputfile=tmpfile_name)
                subprocess.call([config.Config.programs['pdf'], tmpfile_name])
            elif args.html:
                tmpfile_name = "{}/{}".format(tmpdir, "tmp.html")
                pypandoc.convert_file(file, "html", outputfile=tmpfile_name)
                subprocess.call(["xdg-open", file])

    else:
        subprocess.call(["xdg-open", file])
