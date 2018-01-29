"""
Construct list of all files and filer them for their filename and content.
"""
import os
import re
import itertools
import pathlib
import frontmatter
import sh

def _filter_folder(folder):
    """
    Return False for all folder names which should not be searched.
    """
    if "__pycache__" in folder:
        return False
    if "/.git" in folder:
        return False
    return True

def _filter_file(path, markdown_only=False):
    """
    Return False for all file names which should be ignored.
    """
    if path.endswith(".md"):
        return True
    if markdown_only:
        return False
    if path.endswith(".swp"):
        return False
    if path.startswith("."):
        return False
    return True

def get_files(paths, markdown_only=False):
    """
    Return list of all filenames that are in the folders to be searched. The
    filenames and folders are filtered.

    paths: the root paths to be searched
    markdown_only: Files except Markdown files (.md) are ignored
    """

    path_walk = itertools.chain.from_iterable([os.walk(p) for p in paths])


    filenames = itertools.chain.from_iterable(
        (
            (
                (root, file)
                for file
                in filenames
            )
            for root, _, filenames
            in path_walk
            if _filter_folder(root)
        )
        )

    filtered_files = [os.path.join(root, path)
                      for root, path
                      in filenames
                      if _filter_file(path, markdown_only=markdown_only)
                     ]


    return filtered_files

def _has_tags(path, tags_values=None, contents=None):
    """
    Search the YAML frontmatter in path, and return True, if it contains all
    tag-value combinations and matches all strings for the body of the text.
    If the file is not readable, return False.

    tags_values: an iterable of tuples of the form (tag,value).
    contents: an iterable of strings that have to match the body of the file
    """
    try:
        post = frontmatter.load(path)
        if not tags_values is None:
            for tag, value in tags_values:
                if not value in post.get(tag, default=[]):
                    return False
        if not contents is None:
            for content in contents:
                if not content.casefold() in post.content.casefold():
                    return False
        return True
    except:
        return False

def _has_content(path, content, case_sensitive=False):
    try:
        if case_sensitive:
            sh.grep(content, path)
        else:
            sh.grep("-i",content, path)
        return True
    except:
        return False

def filter_content(files, content, case_sensitive=False):
    """
    Filter files using grep.

    case_sensitive: make search case sensitive
    """
    return [f
            for f
            in files
            if _has_content(f, content, case_sensitive=case_sensitive)
           ]

def filter_tags(files, tags_values=None, contents=None):
    """
    Search the YAML frontmatters in files, and return those that contain all
    tag-value combinations.

    tags_values: an iterable of tuples of the form (tag,value).
    """
    return [f
            for f
            in files
            if _has_tags(f, tags_values=tags_values, contents=contents)
           ]

def filter_filename(files, expression):
    """
    Filter the filenames that match expression and ranks them by the quality of
    the match.
    """
    suggestions = []
    pattern = '.*?'.join(expression)   # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern, re.IGNORECASE)  # Compiles a regex.
    for item in files:
        # Checks if the current item matches the regex.
        match = regex.search(pathlib.Path(item).name)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]

def get_tags(files):
    """
    Construct a set of tags present in the files.
    """
    tags = set()

    for file in files:
        try:
            post = frontmatter.load(file)
            for tag in post.get('tags', default=[]):
                tags.add(tag)
        except:
            pass
    return tags
