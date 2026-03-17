"""
输入验证函数模块
"""
import re
from datetime import datetime
from typing import Tuple


def validate_student_id(student_id: str) -> Tuple[bool, str]:
    """校验学号：8位纯数字"""
    if not student_id:
        return False, "学号不能为空"
    
    if not student_id.isdigit():
        return False, "学号必须为纯数字"
    
    if len(student_id) != 8:
        return False, f"学号必须为8位数字，当前为{len(student_id)}位"
    
    return True, "校验通过"


def validate_name(name: str) -> Tuple[bool, str]:
    """校验姓名：非空，最多20字符"""
    if not name or not name.strip():
        return False, "姓名不能为空"
    
    name = name.strip()
    
    if len(name) > 20:
        return False, f"姓名最多20个字符，当前为{len(name)}个字符"
    
    return True, "校验通过"


def validate_gender(gender: str) -> Tuple[bool, str]:
    """校验性别：只允许男/女/其他"""
    from utils.config import ALLOWED_GENDERS
    
    if not gender:
        return False, "性别不能为空"
    
    if gender not in ALLOWED_GENDERS:
        return False, f"性别只允许: {'/'.join(ALLOWED_GENDERS)}"
    
    return True, "校验通过"


def validate_birth_date(birth_date: str) -> Tuple[bool, str]:
    """校验出生年月：格式 YYYY-MM"""
    if not birth_date:
        return False, "出生年月不能为空"
    
    pattern = r'^\d{4}-(0[1-9]|1[0-2])$'
    if not re.match(pattern, birth_date):
        return False, "出生年月格式错误，应为 YYYY-MM"
    
    try:
        year, month = map(int, birth_date.split('-'))
        current_year = datetime.now().year
        
        if year < 1950 or year > current_year:
            return False, f"出生年份应在 1950-{current_year} 之间"
        
    except ValueError:
        return False, "出生年月格式错误"
    
    return True, "校验通过"


def validate_class_name(class_name: str) -> Tuple[bool, str]:
    """校验班级：格式如 高一(3)班"""
    if not class_name:
        return False, "班级不能为空"
    
    from utils.config import CLASS_PATTERN
    
    if not re.match(CLASS_PATTERN, class_name):
        return False, "班级格式错误，如: 高一(3)班 或 高二（5）班"
    
    return True, "校验通过"


def validate_enrollment_year(year: str) -> Tuple[bool, str]:
    """校验入学年份：格式 YYYY"""
    if not year:
        return False, "入学年份不能为空"
    
    if not year.isdigit() or len(year) != 4:
        return False, "入学年份格式错误，应为4位数字 YYYY"
    
    try:
        year_int = int(year)
        current_year = datetime.now().year
        
        if year_int < 2000 or year_int > current_year + 1:
            return False, f"入学年份应在 2000-{current_year + 1} 之间"
        
    except ValueError:
        return False, "入学年份格式错误"
    
    return True, "校验通过"
