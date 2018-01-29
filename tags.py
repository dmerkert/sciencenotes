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
import files
import find

def get_parser(sub_parser,parent_parsers):
    parser = sub_parser.add_parser(
        'tags',
        help="lists all the tags used",
        aliases=['t'],
        parents=parent_parsers
        )

    parser.set_defaults(func=tags)

    return parser

def tags(args):
    filenames = find.find(args, choose=False)
    tag_list = files.get_tags(filenames)
    for tag in sorted(tag_list):
        print(tag)
