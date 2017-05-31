import json


class Singleton(type):
    # Singleton pattern
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ResourceManager(metaclass=Singleton):
    def __init__(self):
        print("Resource Manager Loaded")
        with open("string_resources.json") as f:
            self._str_res = json.load(f)

    def __getitem__(self, key):
        return self._str_res[key]
