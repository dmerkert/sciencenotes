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
