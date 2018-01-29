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
