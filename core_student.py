"""
学生数据类模块 - 定义Student数据类及业务规则校验

本模块包含：
- Student 数据类定义
- 学生信息的业务规则校验
- 学生对象的创建与字段更新
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict

from utils.validators import (
    validate_student_id,
    validate_name,
    validate_gender,
    validate_birth_date,
    validate_class_name,
    validate_enroll_year,
    validate_field,
)
from utils.config import (
    FIELD_STUDENT_ID,
    FIELD_NAME,
    FIELD_GENDER,
    FIELD_BIRTH_DATE,
    FIELD_CLASS_NAME,
    FIELD_ENROLL_YEAR,
    ALL_FIELDS,
)


@dataclass
class Student:
    """
    学生数据类
    
    Attributes:
        student_id: 学号（8位数字）
        name: 姓名
        gender: 性别（男/女/其他）
        birth_date: 出生年月（YYYY-MM格式）
        class_name: 班级名称
        enroll_year: 入学年份
    """
    student_id: str
    name: str
    gender: str
    birth_date: str
    class_name: str
    enroll_year: str
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将Student对象转换为字典
        
        Returns:
            Dict[str, Any]: 学生信息字典
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """
        从字典创建Student对象
        
        Args:
            data: 学生信息字典
            
        Returns:
            Student: 学生对象
        """
        return cls(
            student_id=data.get(FIELD_STUDENT_ID, ""),
            name=data.get(FIELD_NAME, ""),
            gender=data.get(FIELD_GENDER, ""),
            birth_date=data.get(FIELD_BIRTH_DATE, ""),
            class_name=data.get(FIELD_CLASS_NAME, ""),
            enroll_year=data.get(FIELD_ENROLL_YEAR, ""),
        )
    
    def update_field(self, field_name: str, value: str) -> Tuple[bool, str]:
        """
        更新指定字段的值
        
        Args:
            field_name: 字段名称
            value: 新值
            
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        is_valid, error_msg = validate_field(field_name, value)
        if not is_valid:
            return False, error_msg
        
        if field_name == FIELD_STUDENT_ID:
            self.student_id = value
        elif field_name == FIELD_NAME:
            self.name = value
        elif field_name == FIELD_GENDER:
            self.gender = value
        elif field_name == FIELD_BIRTH_DATE:
            self.birth_date = value
        elif field_name == FIELD_CLASS_NAME:
            self.class_name = value
        elif field_name == FIELD_ENROLL_YEAR:
            self.enroll_year = value
        else:
            return False, f"未知字段：{field_name}"
        
        return True, ""


def create_student(
    student_id: str,
    name: str,
    gender: str,
    birth_date: str,
    class_name: str,
    enroll_year: str
) -> Tuple[Optional[Student], str]:
    """
    创建学生对象并进行完整验证
    
    Args:
        student_id: 学号
        name: 姓名
        gender: 性别
        birth_date: 出生年月
        class_name: 班级名称
        enroll_year: 入学年份
        
    Returns:
        Tuple[Optional[Student], str]: (学生对象或None, 错误信息)
    """
    validations = [
        (FIELD_STUDENT_ID, student_id, validate_student_id),
        (FIELD_NAME, name, validate_name),
        (FIELD_GENDER, gender, validate_gender),
        (FIELD_BIRTH_DATE, birth_date, validate_birth_date),
        (FIELD_CLASS_NAME, class_name, validate_class_name),
        (FIELD_ENROLL_YEAR, enroll_year, validate_enroll_year),
    ]
    
    for field_name, value, validator in validations:
        is_valid, error_msg = validator(value)
        if not is_valid:
            return None, error_msg
    
    student = Student(
        student_id=student_id.strip(),
        name=name.strip(),
        gender=gender.strip(),
        birth_date=birth_date.strip(),
        class_name=class_name.strip(),
        enroll_year=str(enroll_year).strip(),
    )
    
    return student, ""


def validate_student_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证学生数据字典是否完整且合法
    
    Args:
        data: 学生数据字典
        
    Returns:
        Tuple[bool, str]: (是否合法, 错误信息)
    """
    for field in ALL_FIELDS:
        if field not in data:
            return False, f"缺少必填字段：{field}"
    
    for field in ALL_FIELDS:
        is_valid, error_msg = validate_field(field, data[field])
        if not is_valid:
            return False, error_msg
    
    return True, ""
