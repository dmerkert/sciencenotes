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
import yaml
import pathlib
import os

def get_parser(argparse):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '--config',
        action="store",
        default=None
        )

    return parser

class Config:
    __slots__ = []   # prevents additional attributes from being added to instances and same-named attributes from shadowing the class's attributes


    path = ""
    programs = {}
    searchpath = []

    @classmethod
    def parseConfig(cls,file="{}/.config/science.yml".format(pathlib.Path.home())):
        with open(file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        cls.path = cfg.get(
                'path',
                "{}/.sciencenotes".format(pathlib.Path.home())
                )
        cls.programs = cfg.get(
                'programs',
                {'pdf': 'okular', 'html': 'chrome', 'editor': 'gedit'}
                )
        cls.searchpath = cfg.get(
                'searchpaths',
                []
                )

        try:
            os.makedirs(cls.path)
        except FileExistsError:
            pass

    @classmethod
    def getPath(cls):
        return cls.path

    @classmethod
    def getPrograms(cls):
        return cls.programs

    @classmethod
    def getSearchpath(cls):
        return cls.searchpath
