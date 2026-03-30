#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

import os
import sys
import platform
from pathlib import Path

from loguru import logger

logger_name = Path(sys.argv[0]).stem
work_path = Path(__file__).parent.parent
log_path = work_path / "log"
log_path.mkdir(exist_ok=True)
log_file = log_path / f"{logger_name}.log"

level = os.getenv("LOG_LEVEL", "INFO")
rotation = os.getenv("LOG_ROTATION", "00:00")
retention = os.getenv("LOG_RETENTION", "10 days")

try:
    logger.add(
        log_file,
        filter="",
        level=level,
        rotation=rotation,
        retention=retention,
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )
except PermissionError as e:
    logger.warning(f"无法写入日志文件 {log_file}: {e}")
except Exception as e:
    logger.warning(f"日志配置失败: {e}")

logger.debug(f"SYSTEM:{platform.platform()}")
logger.debug(f"PYTHON:{sys.version}")
logger.debug(f"LOG: {log_path} [{level}]")

__all__ = ["logger"]
