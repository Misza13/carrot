from carrot.data import Automappable, Autoproperty


class CarrotModel(Automappable):
    def __init__(self):
        self.version = Autoproperty(int, 1)
        self.name = Autoproperty(str, '')
        self.mc_version = Autoproperty(str)
        self.channel = Autoproperty(str, 'Beta')
        self.mods = Autoproperty(InstalledModModel, [], True)


class InstalledModModel(Automappable):
    def __init__(self):
        self.key = Autoproperty(str)
        self.id = Autoproperty(int)
        self.name = Autoproperty(str)
        self.mod_source = Autoproperty(str)
        self.installed_as = Autoproperty(str)
        self.file = Autoproperty(ModFileModel)


class ModFileModel(Automappable):
    def __init__(self):
        self.file_name = Autoproperty(str)
