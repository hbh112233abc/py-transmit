#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"


import sys
import platform
from pathlib import Path

from loguru import logger

level = "INFO"

logger_name = Path(sys.argv[0]).stem
work_path = Path(sys.argv[0]).parent
log_path = work_path / "log"
log_path.mkdir(exist_ok=True)
log_file = log_path / f"{logger_name}.log"

logger.add(
    log_file,
    filter="",
    level=level,
    rotation="00:00",
    retention="10 days",
    backtrace=True,
    diagnose=True,
)

logger.info(f"SYSTEM:{platform.platform()}")
logger.info(f"PYTHON:{sys.version}")
logger.info(f"LOG: {log_path} [{level}]")
