import datetime
import os
import pathlib
import re
# import sys
import subprocess
import sh
import tempfile
import pypandoc
import config
import yaml

cfg = config.Config()

def generateFilename(name,extension=".md"):
    filename = "{}-{}{}".format(
            datetime.date.today().strftime("%Y-%m-%d"),
            name,
            extension
            )
    filepath = "{}/{}/{}".format(
            cfg.getPath(),
            datetime.date.today().strftime("%Y"),
            datetime.date.today().strftime("%m")
            )
    fullfilepath = "{}/{}".format(filepath,filename)

    try:
        os.makedirs(filepath)
    except FileExistsError:
        pass

    return fullfilepath

def create(name):
    
    fullfilepath = generateFilename(name)

    pathlib.Path(fullfilepath).touch()
    return fullfilepath

def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = '.*?'.join(user_input)   # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern,re.IGNORECASE)  # Compiles a regex.
    for item in collection:
        match = regex.search(item.replace(cfg.path,""))   # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]

def getFilesInDir(filterMarkdown=False,otherSearchPaths=False):
    gitRe = re.compile(".git$|.git/")
    binRe = re.compile("/bin$|/__pycache__$")

    files = []
    for root, directories, filenames in os.walk(cfg.getPath()):
        if not gitRe.search(root) and not binRe.search(root):
            for filename in filenames:
                if not filterMarkdown or filename.endswith(".md"):
                    files.append(os.path.join(root,filename))

    if otherSearchPaths:
        for p in cfg.getSearchpath():
            for root, directories, filenames in os.walk(p):
                if not gitRe.search(root) and not binRe.search(root):
                    for filename in filenames:
                        if not filterMarkdown or filename.endswith(".md"):
                            files.append(os.path.join(root,filename))

    return files

def find(
        string,
        filterMarkdown=False,
        otherSearchPaths=False,
        n=None,
        grep=False,
        fuzzy=False,
        tags=False
        ):

    finds = []
    if fuzzy or tags:
        files = getFilesInDir(filterMarkdown=filterMarkdown,otherSearchPaths=otherSearchPaths)
        if fuzzy:
            for f in fuzzyfinder(string,files):
                finds.append(f)
        if tags:
            for f in find_tags(string,files):
                finds.append(f)
    if grep:
        for f in find_grep(string):
            finds.append(f)

    if n != None:
        if n < 0:
            print("n HAS TO BE POSITIVE")
            return None
        if n >= len(finds):
            print("n IS TOO LARGE")
            return None
        else:
            return finds[n]

    if len(finds) == 0:
        print("NO FILE FOUND")
    elif len(finds) > 1:
        for i,f in enumerate(finds):
            print("{}: {}".format(i,f))
    else:
        return finds[0]
    return None


def view(file):
    if file != None:
        if file.endswith(".md"):
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpfileName = "{}/{}".format(tmpdir,"tmp.pdf")
                pypandoc.convert_file(file,"pdf",outputfile=tmpfileName)
                subprocess.call([cfg.programs['pdf'],tmpfileName])
        else:
            subprocess.call(["xdg-open", file])


def edit(file):
    if file != None:
        subprocess.call([cfg.getPrograms()['editor'],file])

def find_grep(file):
    try:
        output = sh.grep(
                '-lirs',
                "--exclude-dir=.git",
                "--exclude=.*.swp",
                file,
                cfg.getPath()
                )
        return [o for o in output.splitlines()]
    except sh.ErrorReturnCode:
        return []

def update():
    try:
        val = sh.git("-C",cfg.getPath(),"pull","origin","master")
    except sh.ErrorReturnCode:
        print(val)
        return
    try:
        val = sh.git("-C",cfg.getPath(),"add","-A")
    except sh.ErrorReturnCode:
        print(val)
        return
    try:
        val = sh.git("-C",cfg.getPath(),"commit","-a","-m","update")
    except sh.ErrorReturnCode:
        print(val)
        return
    try:
        val = sh.git("-C",cfg.getPath(),"push","origin","master")
    except sh.ErrorReturnCode:
        print(val)
        return

def find_tags(string,files):

    finds = []
    for file in files:
        with open(file) as f:
            y = next(yaml.load_all(f))
            if string in y['tags']:
                finds.append(file)

    return finds


