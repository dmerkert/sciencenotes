"""
Creates a parser for finding files and applies the options to filter the files.
"""
import config
import files

def get_parser(argparse):
    """
    Construt a parser for searching files using argparse.
    """
    parser = argparse.ArgumentParser(add_help=False)

    #fuzzy search on the file name
    parser.add_argument(
        'filename',
        action='store',
        help='filters files which name matches a fuzzy search',
        nargs='?',
        default=None)

    #use the n-th match
    parser.add_argument(
        'N',
        type=int,
        action='store',
        help='use the N-th item found',
        nargs='?',
        default=None)

    #grep content
    parser.add_argument(
        '-g',
        '--grep',
        action='store',
        dest='grep',
        default=None,
        help='filter files for their content using grep'
        )

    #filter content of text files
    parser.add_argument(
        '-c',
        '--content',
        action='store',
        dest='content',
        default=None,
        nargs='*',
        help='filter files for their content in case of text files'
        )

    #author
    parser.add_argument(
        '-a',
        '--author',
        action='store',
        dest='author',
        default=None,
        help='filter for author'
        )

    #title
    parser.add_argument(
        '--title',
        action='store',
        dest='title',
        default=None,
        help='filter for title'
        )

    #type
    parser.add_argument(
        '--type',
        action='store',
        dest='type',
        default=None,
        help='filter for type'
        )

    #tags
    parser.add_argument(
        '-t',
        '--tags',
        action='store',
        dest='tags',
        default=None,
        nargs='+',
        help='filter for tags'
        )

    #Other search paths
    parser.add_argument(
        '--other',
        action="store_true",
        default=False,
        help="search other search paths"
        )

    return parser

def return_file_choice(filenames, N):
    """
    Given a list of filenames, the N-th is chosen, if there are more than one.
    If N is None, a list is displayed, if the choice is not trivial.
    """

    if not N is None:
        if N >= len(filenames):
            print("N is too large.")
            return None

    if not filenames:
        print("No files found matching the criteria.")
        return None
    elif len(filenames) == 1:
        if N is None:
            return filenames[0]
        elif N == 0:
            return filenames[0]
    else:
        if N is None:
            for i, file in enumerate(filenames):
                print("{}: {}".format(i, file))
            return None
        return filenames[N]



def find(args, markdown_only=False):
    """
    Applies filters to obtain a file of the user's choice.

    markdown_only: considers only files ending in .md
    """

    paths = [config.Config.getPath()]
    if args.other:
        paths.extend(config.Config.getSearchpath())

    #get list of files in dirs
    filenames = files.get_files(paths, markdown_only=markdown_only)

    #filter for fuzzy string
    if not args.filename is None:
        filenames = files.filter_filename(filenames, args.filename)

    #filter for tags (author, title, type, tags)
    #filter for content
    tag_list = []
    if not args.author is None:
        tag_list.append(("author", args.author))
    if not args.title is None:
        tag_list.append(("title", args.title))
    if not args.type is None:
        tag_list.append(("type", args.type))
    if not args.tags is None:
        if not isinstance(args.tags, list):
            raise ValueError("This is not a list")
        for tag in args.tags:
            tag_list.append(("tags", tag))
    if not tag_list:
        tag_list = None

    if (not tag_list is None) or (not args.content is None):
        filenames = files.filter_tags(
            filenames,
            tags_values=tag_list,
            contents=args.content)

    #filter for grep
    if not args.grep is None:
        filenames = files.filter_content(filenames, args.grep)

    return return_file_choice(filenames, args.N)
