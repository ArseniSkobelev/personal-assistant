class ConfigException(Exception):
    def __init__(self, message):
        super().__init__(message)


class KubernetesException(Exception):
    def __init__(self, message):
        super().__init__(message)


class DatabaseException(Exception):
    def __init__(self, message):
        super().__init__(message)
