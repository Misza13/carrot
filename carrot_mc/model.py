from carrot_mc.data import Automappable, Autoproperty


class CarrotModel(Automappable):
    def __init__(self):
        self.version = Autoproperty(int, 1)
        self.name = Autoproperty(str, '')
        self.mc_version = Autoproperty(str)
        self.channel = Autoproperty(str, 'Beta')
        self.mods = Autoproperty(InstalledModModel, [], True)


class BaseModModel(Automappable):
    def __init__(self):
        self.key = Autoproperty(str)
        self.id = Autoproperty(int)
        self.name = Autoproperty(str)
        self.owner = Autoproperty(str)
        self.blurb = Autoproperty(str)
        self.file = Autoproperty(ModFileModel)


class InstalledModModel(BaseModModel):
    def __init__(self):
        super().__init__()
        self.mod_source = Autoproperty(str)
        self.dependency = Autoproperty(bool)


class ModModel(BaseModModel):
    def __init__(self):
        super().__init__()
        self.download_count = Autoproperty(int)
        self.categories = Autoproperty(list, [])


class ModFileModel(Automappable):
    def __init__(self):
        self.id = Autoproperty(int)
        self.download_url = Autoproperty(str)
        self.file_name = Autoproperty(str)
        self.file_md5 = Autoproperty(str)
        self.release_type = Autoproperty(str)
        self.mod_dependencies = Autoproperty(list, [])
