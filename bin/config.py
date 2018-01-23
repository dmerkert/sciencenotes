import yaml
import pathlib
import os

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
