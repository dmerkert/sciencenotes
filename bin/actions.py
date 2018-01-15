import datetime
import os
import pathlib
import re
# import sys
import subprocess
import tempfile
import pypandoc
import config as cfg

def create(name):
    filename = "{}-{}.md".format(
            datetime.date.today().strftime("%Y-%m-%d"),
            name
            )
    filepath = "{}/{}/{}".format(
            cfg.path,
            datetime.date.today().strftime("%Y"),
            datetime.date.today().strftime("%m")
            )
    fullfilepath = "{}/{}".format(filepath,filename)

    try:
        os.makedirs(filepath)
    except FileExistsError:
        pass
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

def getFilesInDir():
    gitRe = re.compile(".git$|.git/")
    binRe = re.compile("bin$")

    files = []
    for root, directories, filenames in os.walk(cfg.path):
        if not gitRe.search(root) and not binRe.search(root):
            for filename in filenames: 
                files.append(os.path.join(root,filename))
    return files

def find(string):
    files = getFilesInDir()
    finds = fuzzyfinder(string,files)
    if len(finds) == 0:
        print("NO FILE FOUND")
    elif len(finds) > 1:
        for f in finds:
            print(f)
    else:
        return finds[0]
    return None

def view(file):
    # file = find(string)
    if file != None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfileName = "{}/{}".format(tmpdir,"tmp.pdf")
            pypandoc.convert_file(file,"pdf",outputfile=tmpfileName)
            subprocess.call([cfg.programs['pdf'],tmpfileName])

def edit(file):
    # file = find(string)
    if file != None:
        subprocess.call([cfg.programs['editor'],file])
