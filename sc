#!/usr/bin/env python

"""
Science notes: organizes notes for scientific purposes and searches them
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

import argument_parser
import config

parsed_args = argument_parser.parse()


cfg = config.Config()
if hasattr(parsed_args, 'config') and not parsed_args.config is None:
    cfg.parseConfig(file=parsed_args.config)
else:
    cfg.parseConfig()

argument_parser.callAction(parsed_args)
