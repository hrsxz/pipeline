import logging

# 配置日志格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"


# 配置日志系统
def setup_logger(name: str = "main_logger", level=logging.INFO) -> logging.Logger:
    """
    配置日志记录器
    Args:
        name (str): 日志记录器的名称
        level (int): 日志记录级别
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 配置控制台日志输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # 配置日志格式
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)

    # 避免重复添加处理程序
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger
