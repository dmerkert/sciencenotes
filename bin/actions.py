import datetime
import os
import pathlib
import re
# import sys
import subprocess
import tempfile
import pypandoc
import config

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
    binRe = re.compile("bin$")

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

def find(string,filterMarkdown=False,otherSearchPaths=False):
    files = getFilesInDir(filterMarkdown=filterMarkdown,otherSearchPaths=otherSearchPaths)
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

def grep(file):
    command = ["grep", "-lirs","--exclude-dir=.git","--exclude=.*.swp",file,
            cfg.getPath()]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code == 0:
        return [o.decode('utf-8') for o in output.splitlines()]
    else:
        return []
