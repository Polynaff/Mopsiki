class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
        return cls._instance

    def set_option(self, key, value):
        self.config[key] = value

    def get_option(self, key, default=None):
        return self.config.get(key, default)


if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()
    s1.set_option("mode", "debug")
    print(s1 is s2)
    print(s2.get_option("mode"))
