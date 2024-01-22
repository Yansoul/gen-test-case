# coding: utf-8

from typing import List

from pydantic import BaseModel, Field


# 输出模板
class TestPoint(BaseModel):
    category: str = Field(description="测试点所属的维度")
    content: str = Field(description="测试点的内容")


class TestPointSet(BaseModel):
    test_points: List[TestPoint]


class TestCase(BaseModel):
    """
    "用例描述": "${Field} 字段上送错误的值，验证常规性校验",
    "正例/反例": "反例",
    "步骤说明": "${Explain}",
    "预期结果": "查询失败，提示信息合理"
    """
    用例描述: str = Field(description="测试用例的描述")
    正反例: str = Field(description="正例/反例")
    步骤说明: str = Field(description="测试用例步骤说明")
    预期结果: str = Field(description="测试用例预期结果")


class TestCaseSet(BaseModel):
    测试用例集: List[TestCase]