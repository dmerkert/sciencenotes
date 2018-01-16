import yaml

class Config:
    __slots__ = []   # prevents additional attributes from being added to instances and same-named attributes from shadowing the class's attributes


    path = ""
    programs = {}
    searchpath = []

    @classmethod
    def parseConfig(cls,file="config.yml"):
        with open(file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        cls.path = cfg['path']
        cls.programs = cfg['programs']
        cls.searchpaths = cfg['searchpaths']

    @classmethod
    def getPath(cls):
        return cls.path

    @classmethod
    def getPrograms(cls):
        return cls.programs

    @classmethod
    def getSearchpath(cls):
        return cls.searchpath
