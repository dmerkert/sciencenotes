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

