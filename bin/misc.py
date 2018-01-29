import os
import datetime
import config

def generate_filename(name, extension=".md"):
    filename = name.replace(" ", "_")
    filename = "{}-{}{}".format(
        datetime.date.today().strftime("%Y-%m-%d"),
        filename,
        extension
        )
    filepath = "{}/{}/{}".format(
        config.Config.getPath(),
        datetime.date.today().strftime("%Y"),
        datetime.date.today().strftime("%m")
        )
    fullfilepath = "{}/{}".format(filepath, filename)

    try:
        os.makedirs(filepath)
    except FileExistsError:
        pass

    return fullfilepath
