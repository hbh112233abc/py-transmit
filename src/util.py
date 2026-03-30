#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

from typing import Any, Literal

from pydantic import BaseModel, Field


class Result(BaseModel):
    """通用响应结果模型

    用于统一 API 响应格式，包含状态码、消息和返回数据。

    Attributes:
        code: 结果状态码，0 表示成功，1 表示失败
        msg: 响应消息，描述操作结果或错误信息
        data: 返回数据，可以是任意类型

    Example:
        >>> Result.success(data={"id": 1})
        >>> Result.error(msg="参数错误")
    """

    code: Literal[0, 1] = Field(0, description="Result code 0:success 1:error")
    msg: str = Field("", description="Result message")
    data: Any = Field(None, description="Result data")

    @classmethod
    def success(
        cls, data: Any = None, msg: str = "操作成功", code: int = 0
    ) -> "Result":
        """创建成功响应"""
        return cls(code=code, msg=msg, data=data)

    @classmethod
    def error(cls, msg: str = "操作失败", code: int = 1, data: Any = None) -> "Result":
        """创建失败响应"""
        return cls(code=code, msg=msg, data=None)
