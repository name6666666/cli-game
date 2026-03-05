class CliGameError(Exception):
    pass

class ClassNameError(CliGameError):
    pass

class BorderError(CliGameError):
    pass

class CharWidthError(CliGameError):
    pass

class StorageNameError(CliGameError):
    pass

class GroupError(CliGameError):
    pass
