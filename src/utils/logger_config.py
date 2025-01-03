import logging
import os

# 配置日志格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"


# 配置日志系统
def setup_logger(
    name: str = "main_logger", level=logging.INFO, filename=""
) -> logging.Logger:
    """
    Config the logger with the given name and level.
    Args:
        name (str): 日志记录器的名称
        level (int): 日志记录级别
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create log file
    if filename != "":
        log_dir = os.path.dirname(filename)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        # file output
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)

    # console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
