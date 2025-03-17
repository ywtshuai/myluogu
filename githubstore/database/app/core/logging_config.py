import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    # 创建logs目录（如果不存在）
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 设置日志格式
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 设置文件处理器
    file_handler = logging.handlers.RotatingFileHandler(
        filename=f'logs/app_{datetime.now().strftime("%Y%m%d")}.log',
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_format)

    # 设置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # 设置特定模块的日志级别
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)