from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass


class FileLogger(Logger):
    def log(self, message):
        print("[FILE]", message)


class ConsoleLogger(Logger):
    def log(self, message):
        print("[CONSOLE]", message)


class LoggerFactory(ABC):
    @abstractmethod
    def create_logger(self):
        pass

    def log_message(self, message):
        logger = self.create_logger()
        logger.log(message)


class FileLoggerFactory(LoggerFactory):
    def create_logger(self):
        return FileLogger()


class ConsoleLoggerFactory(LoggerFactory):
    def create_logger(self):
        return ConsoleLogger()


if __name__ == "__main__":
    file_factory = FileLoggerFactory()
    console_factory = ConsoleLoggerFactory()
    file_factory.log_message("лог в файл")
    console_factory.log_message("лог в консоль")
