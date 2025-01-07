import logging

class Logger:
    def __init__(self, name: str, log_file: str, level: int = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create handlers
        file_handler = logging.FileHandler(log_file, mode='a')
        console_handler = logging.StreamHandler()

        # Set level for handlers
        file_handler.setLevel(level)
        console_handler.setLevel(level)

        # Create formatters and add them to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)


if __name__ == "__main__":
    # Example usage:
    logger = Logger('my_logger', 'app.log')
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.error('This is an error message')