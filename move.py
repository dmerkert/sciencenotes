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
import os
import pathlib
import shutil
import config
import misc

def get_parser(sub_parser,parent_parsers):
    parser = sub_parser.add_parser(
        'move',
        help="moves a file to the directory",
        aliases=['mv'],
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

    parser.set_defaults(func=move)

    return parser

def move(args):
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

    shutil.move(args.source, fullfilepath)




