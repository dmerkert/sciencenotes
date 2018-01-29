"""
Science Notes: organizes notes for scientific purposes and searches them
Copyright (C) 2018  Dennis Merkert

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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
