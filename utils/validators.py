"""
验证器模块 - 提供各种输入验证函数

本模块包含所有用于验证用户输入的函数，包括：
- 学号验证（8位数字）
- 姓名验证（非空、最大20字符）
- 性别验证（男/女/其他）
- 出生年月验证（YYYY-MM格式）
- 班级名称验证（如"高一（3）班"格式）
- 入学年份验证
"""

import re
from typing import Tuple, Optional

from utils.config import (
    PATTERN_STUDENT_ID,
    PATTERN_BIRTH_DATE,
    PATTERN_CLASS_NAME,
    VALID_GENDERS,
    STUDENT_ID_LENGTH,
    NAME_MAX_LENGTH,
    FIELD_DISPLAY_NAMES,
)


def validate_student_id(student_id: str) -> Tuple[bool, str]:
    """
    验证学号是否合法
    
    Args:
        student_id: 待验证的学号字符串
        
    Returns:
        Tuple[bool, str]: (是否合法, 错误信息)
    """
    if not student_id:
        return False, f"{FIELD_DISPLAY_NAMES.get('student_id', '学号')}不能为空"
    
    student_id = student_id.strip()
    
    if not re.match(PATTERN_STUDENT_ID, student_id):
        return False, f"{FIELD_DISPLAY_NAMES.get('student_id', '学号')}必须为{STUDENT_ID_LENGTH}位纯数字"
    
    return True, ""


def validate_name(name: str) -> Tuple[bool, str]:
    """
    验证姓名是否合法
    
    Args:
        name: 待验证的姓名字符串
        
    Returns:
        Tuple[bool, str]: (是否合法, 错误信息)
    """
    if not name:
        return False, f"{FIELD_DISPLAY_NAMES.get('name', '姓名')}不能为空"
    
    name = name.strip()
    
    if len(name) == 0:
        return False, f"{FIELD_DISPLAY_NAMES.get('name', '姓名')}不能为空"
    
    if len(name) > NAME_MAX_LENGTH:
        return False, f"{FIELD_DISPLAY_NAMES.get('name', '姓名')}长度不能超过{NAME_MAX_LENGTH}个字符"
    
    return True, ""


def validate_gender(gender: str) -> Tuple[bool, str]:
    """
    验证性别是否合法
    
    Args:
        gender: 待验证的性别字符串
        
    Returns:
        Tuple[bool, str]: (是否合法, 错误信息)
    """
    if not gender:
        return False, f"{FIELD_DISPLAY_NAMES.get('gender', '性别')}不能为空"
    
    gender = gender.strip()
    
    if gender not in VALID_GENDERS:
        return False, f"{FIELD_DISPLAY_NAMES.get('gender', '性别')}只能是：{'/'.join(VALID_GENDERS)}"
    
    return True, ""


def validate_birth_date(birth_date: str) -> Tuple[bool, str]:
    """
    验证出生年月是否合法
    
    Args:
        birth_date: 待验证的出生年月字符串（YYYY-MM格式）
        
    Returns:
        Tuple[bool, str]: (是否合法, 错误信息)
    """
    if not birth_date:
        return False, f"{FIELD_DISPLAY_NAMES.get('birth_date', '出生年月')}不能为空"
    
    birth_date = birth_date.strip()
    
    if not re.match(PATTERN_BIRTH_DATE, birth_date):
        return False, f"{FIELD_DISPLAY_NAMES.get('birth_date', '出生年月')}格式错误，正确格式：YYYY-MM"
    
    return True, ""


def validate_class_name(class_name: str) -> Tuple[bool, str]:
    """
    验证班级名称是否合法
    
    Args:
        class_name: 待验证的班级名称字符串
        
    Returns:
        Tuple[bool, str]: (是否合法, 错误信息)
    """
    if not class_name:
        return False, f"{FIELD_DISPLAY_NAMES.get('class_name', '班级')}不能为空"
    
    class_name = class_name.strip()
    
    if not re.match(PATTERN_CLASS_NAME, class_name):
        return False, f"{FIELD_DISPLAY_NAMES.get('class_name', '班级')}格式错误，正确格式如：高一（3）班"
    
    return True, ""


def validate_enroll_year(enroll_year: str) -> Tuple[bool, str]:
    """
    验证入学年份是否合法
    
    Args:
        enroll_year: 待验证的入学年份字符串
        
    Returns:
        Tuple[bool, str]: (是否合法, 错误信息)
    """
    if not enroll_year:
        return False, f"{FIELD_DISPLAY_NAMES.get('enroll_year', '入学年份')}不能为空"
    
    enroll_year = str(enroll_year).strip()
    
    if not re.match(r"^\d{4}$", enroll_year):
        return False, f"{FIELD_DISPLAY_NAMES.get('enroll_year', '入学年份')}必须为4位数字年份"
    
    year = int(enroll_year)
    if year < 1900 or year > 2100:
        return False, f"{FIELD_DISPLAY_NAMES.get('enroll_year', '入学年份')}必须在1900-2100之间"
    
    return True, ""


def validate_field(field_name: str, value: str) -> Tuple[bool, str]:
    """
    根据字段名自动选择对应的验证函数进行验证
    
    Args:
        field_name: 字段名称
        value: 待验证的值
        
    Returns:
        Tuple[bool, str]: (是否合法, 错误信息)
    """
    validators = {
        "student_id": validate_student_id,
        "name": validate_name,
        "gender": validate_gender,
        "birth_date": validate_birth_date,
        "class_name": validate_class_name,
        "enroll_year": validate_enroll_year,
    }
    
    validator = validators.get(field_name)
    if validator:
        return validator(value)
    
    return False, f"未知字段：{field_name}"
