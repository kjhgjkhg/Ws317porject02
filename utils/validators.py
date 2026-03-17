"""
输入验证工具模块

提供各种输入验证函数，包括学号、姓名、日期等格式校验。
"""

import re
from typing import Tuple
from datetime import datetime


def validate_student_id_format(student_id: str) -> Tuple[bool, str]:
    if not student_id:
        return False, "学号不能为空"
    if not re.match(r"^\d{8}$", student_id):
        return False, "学号必须为8位纯数字"
    return True, ""


def validate_name_format(name: str) -> Tuple[bool, str]:
    if not name or not name.strip():
        return False, "姓名不能为空"
    name = name.strip()
    if len(name) > 20:
        return False, "姓名最多20个字符"
    if re.search(r"[\d\s]", name):
        return False, "姓名不能包含数字或特殊空白字符"
    return True, ""


def validate_gender_format(gender: str, allowed: Tuple[str, ...] = ("男", "女", "其他")) -> Tuple[bool, str]:
    if gender not in allowed:
        return False, f"性别只允许: {', '.join(allowed)}"
    return True, ""


def validate_birth_date_format(birth_date: str) -> Tuple[bool, str]:
    if not birth_date:
        return False, "出生年月不能为空"
    
    pattern = r"^\d{4}-(0[1-9]|1[0-2])$"
    if not re.match(pattern, birth_date):
        return False, "出生年月格式错误，应为 YYYY-MM"
    
    try:
        year, month = map(int, birth_date.split("-"))
        current_year = datetime.now().year
        if year < 1900 or year > current_year:
            return False, f"出生年份应在 1900-{current_year} 之间"
        return True, ""
    except ValueError:
        return False, "出生年月格式错误"


def validate_class_name_format(class_name: str) -> Tuple[bool, str]:
    if not class_name or not class_name.strip():
        return False, "班级不能为空"
    
    pattern = r"^[高中初][一二三四五六七八九十零]+[（(][0-9一二三四五六七八九十零]+[)）]班$"
    if not re.match(pattern, class_name):
        return False, "班级格式应为如 '高一（3）班' 或 '初二(1)班'"
    
    return True, ""


def validate_enrollment_year_format(enrollment_year: str) -> Tuple[bool, str]:
    if not enrollment_year:
        return False, "入学年份不能为空"
    
    if not re.match(r"^\d{4}$", enrollment_year):
        return False, "入学年份必须为4位数字"
    
    try:
        year = int(enrollment_year)
        current_year = datetime.now().year
        if year < 1900 or year > current_year + 1:
            return False, f"入学年份应在 1900-{current_year + 1} 之间"
        return True, ""
    except ValueError:
        return False, "入学年份格式错误"


def sanitize_input(value: str) -> str:
    return value.strip()


def is_valid_student_id(student_id: str) -> bool:
    valid, _ = validate_student_id_format(student_id)
    return valid


def is_valid_name(name: str) -> bool:
    valid, _ = validate_name_format(name)
    return valid


def is_valid_gender(gender: str, allowed: Tuple[str, ...] = ("男", "女", "其他")) -> bool:
    valid, _ = validate_gender_format(gender, allowed)
    return valid


def is_valid_birth_date(birth_date: str) -> bool:
    valid, _ = validate_birth_date_format(birth_date)
    return valid


def is_valid_class_name(class_name: str) -> bool:
    valid, _ = validate_class_name_format(class_name)
    return valid


def is_valid_enrollment_year(enrollment_year: str) -> bool:
    valid, _ = validate_enrollment_year_format(enrollment_year)
    return valid
