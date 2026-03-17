"""
配置模块 - 存放所有常量、路径配置和允许值列表

本模块定义了学生信息管理系统中使用的所有常量，包括：
- 数据文件路径
- 字段名称
- 允许的性别选项
- 班级格式正则表达式等
"""

import os
from typing import List, Dict, Any

PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR: str = os.path.join(PROJECT_ROOT, "source_data")
OUTPUT_DIR: str = os.path.join(PROJECT_ROOT, "output_build")

DATA_FILE: str = os.path.join(DATA_DIR, "students.json")
CONFIG_FILE: str = os.path.join(DATA_DIR, ".do_not_touch.cfg")

FIELD_STUDENT_ID: str = "student_id"
FIELD_NAME: str = "name"
FIELD_GENDER: str = "gender"
FIELD_BIRTH_DATE: str = "birth_date"
FIELD_CLASS_NAME: str = "class_name"
FIELD_ENROLL_YEAR: str = "enroll_year"

ALL_FIELDS: List[str] = [
    FIELD_STUDENT_ID,
    FIELD_NAME,
    FIELD_GENDER,
    FIELD_BIRTH_DATE,
    FIELD_CLASS_NAME,
    FIELD_ENROLL_YEAR,
]

FIELD_DISPLAY_NAMES: Dict[str, str] = {
    FIELD_STUDENT_ID: "学号",
    FIELD_NAME: "姓名",
    FIELD_GENDER: "性别",
    FIELD_BIRTH_DATE: "出生年月",
    FIELD_CLASS_NAME: "班级",
    FIELD_ENROLL_YEAR: "入学年份",
}

VALID_GENDERS: List[str] = ["男", "女", "其他"]

STUDENT_ID_LENGTH: int = 8
NAME_MAX_LENGTH: int = 20

PATTERN_STUDENT_ID: str = r"^\d{8}$"
PATTERN_BIRTH_DATE: str = r"^\d{4}-(0[1-9]|1[0-2])$"
PATTERN_CLASS_NAME: str = r"^[高低初][一二三四五六七八九十]{1,2}[（(][0-9一二三四五六七八九十]+[)）]班$"

BORDER_CHAR: str = "-"
BORDER_WIDTH: int = 60

SUCCESS_PREFIX: str = "[成功]"
ERROR_PREFIX: str = "[错误]"
INFO_PREFIX: str = "[信息]"
