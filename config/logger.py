import logging
import os

def configure_logger(name="app_logger", log_dir="logs"):
    # Create logs directory if not exists
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    # Configure the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if os.getenv("DEBUG", "False").lower() in ["true", "1"] else logging.INFO)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Example usage:
# logger = configure_logger()
# logger.info("Logger initialized successfully")
