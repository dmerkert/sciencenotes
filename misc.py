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
import datetime
from dateutil import parser
import config
import sh

def generate_filename(filename, extension=".md",date=None):
    filedate = datetime.date.today()

    if not date is None:
        if isinstance(date, str):
            filedate = parser.parse(date)

    filename = filename.replace(" ", "_")
    filename = "{}-{}{}".format(
        filedate.strftime("%Y-%m-%d"),
        filename,
        extension
        )
    filepath = "{}/{}/{}".format(
        config.Config.getPath(),
        filedate.strftime("%Y"),
        filedate.strftime("%m")
        )
    fullfilepath = "{}/{}".format(filepath, filename)

    try:
        os.makedirs(filepath)
    except FileExistsError:
        pass

    return fullfilepath

def compress_pdf(infile, outfile):
    sh.gs(
        "-dNOPAUSE",
        "-dBATCH",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-sOutputFile={}".format(outfile),
        infile
        )
