import logging

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler for HTML reports
        file_handler = logging.FileHandler('test_logs.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Make sure logs appear in pytest output
        logger.propagate = True

    return logger
