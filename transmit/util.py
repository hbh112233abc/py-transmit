#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

from typing import Any, Literal

from pydantic import BaseModel, Field


class Result(BaseModel):
    code: Literal[0, 1] = Field(0, description="Result code 0:success 1:error")
    msg: str = Field("", description="Result message")
    data: Any = Field(None, description="Result data")
