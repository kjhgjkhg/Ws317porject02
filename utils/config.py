"""
配置常量模块

定义系统中使用的常量，包括字段名、文件路径、允许值列表等。
"""

import os
from typing import Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "source_data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_build")

DATA_FILE = os.path.join(DATA_DIR, "students.json")
CONFIG_FILE = os.path.join(DATA_DIR, ".do_not_touch.cfg")

FIELD_NAMES: Tuple[str, ...] = (
    "student_id",
    "name",
    "gender",
    "birth_date",
    "class_name",
    "enrollment_year"
)

FIELD_LABELS = {
    "student_id": "学号",
    "name": "姓名",
    "gender": "性别",
    "birth_date": "出生年月",
    "class_name": "班级",
    "enrollment_year": "入学年份"
}

VALID_GENDERS: Tuple[str, ...] = ("男", "女", "其他")

STUDENT_ID_LENGTH = 8
NAME_MAX_LENGTH = 20
BIRTH_DATE_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])$"
CLASS_NAME_PATTERN = r"^[高中初][一二三四五六七八九十零]+[（(][0-9一二三四五六七八九十零]+[)）]班$"

MIN_ENROLLMENT_YEAR = 1900

DATA_FILE_ENCODING = "utf-8"
JSON_INDENT = 2

MENU_OPTIONS = {
    "1": "添加学生",
    "2": "删除学生",
    "3": "修改学生信息",
    "4": "查询学生",
    "5": "列出所有学生",
    "6": "统计信息",
    "0": "退出系统"
}

SORT_OPTIONS = {
    "1": "enrollment_year",
    "2": "class_name",
    "3": "student_id"
}

SEARCH_OPTIONS = {
    "1": "student_id",
    "2": "name",
    "3": "class_name",
    "4": "combined"
}
