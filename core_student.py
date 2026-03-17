"""
学生数据类与业务规则校验模块
"""
from typing import Dict, Optional, Any
from datetime import datetime
from utils.validators import (
    validate_student_id,
    validate_name,
    validate_gender,
    validate_birth_date,
    validate_class_name,
    validate_enrollment_year
)


class Student:
    """学生数据类"""
    
    FIELD_NAMES = ['student_id', 'name', 'gender', 'birth_date', 'class_name', 'enrollment_year']
    
    def __init__(
        self,
        student_id: str,
        name: str,
        gender: str,
        birth_date: str,
        class_name: str,
        enrollment_year: str
    ):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.class_name = class_name
        self.enrollment_year = enrollment_year
    
    def to_dict(self) -> Dict[str, str]:
        """转换为字典"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'class_name': self.class_name,
            'enrollment_year': self.enrollment_year
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Student':
        """从字典创建学生对象"""
        return cls(
            student_id=data.get('student_id', ''),
            name=data.get('name', ''),
            gender=data.get('gender', ''),
            birth_date=data.get('birth_date', ''),
            class_name=data.get('class_name', ''),
            enrollment_year=data.get('enrollment_year', '')
        )
    
    def __str__(self) -> str:
        """字符串表示"""
        return (
            f"学号: {self.student_id} | 姓名: {self.name} | "
            f"性别: {self.gender} | 出生年月: {self.birth_date} | "
            f"班级: {self.class_name} | 入学年份: {self.enrollment_year}"
        )


class StudentValidator:
    """学生数据校验器"""
    
    @staticmethod
    def validate_all(
        student_id: str,
        name: str,
        gender: str,
        birth_date: str,
        class_name: str,
        enrollment_year: str,
        existing_ids: Optional[set] = None,
        is_update: bool = False
    ) -> tuple[bool, str]:
        """
        校验所有字段
        返回: (是否通过, 错误信息)
        """
        existing_ids = existing_ids or set()
        
        sid_valid, sid_msg = validate_student_id(student_id)
        if not sid_valid:
            return False, f"学号错误: {sid_msg}"
        
        if not is_update and student_id in existing_ids:
            return False, f"学号错误: 学号 {student_id} 已存在，不可重复"
        
        name_valid, name_msg = validate_name(name)
        if not name_valid:
            return False, f"姓名错误: {name_msg}"
        
        gender_valid, gender_msg = validate_gender(gender)
        if not gender_valid:
            return False, f"性别错误: {gender_msg}"
        
        birth_valid, birth_msg = validate_birth_date(birth_date)
        if not birth_valid:
            return False, f"出生年月错误: {birth_msg}"
        
        class_valid, class_msg = validate_class_name(class_name)
        if not class_valid:
            return False, f"班级错误: {class_msg}"
        
        year_valid, year_msg = validate_enrollment_year(enrollment_year)
        if not year_valid:
            return False, f"入学年份错误: {year_msg}"
        
        return True, "校验通过"
    
    @staticmethod
    def validate_field(field_name: str, value: str) -> tuple[bool, str]:
        """校验单个字段"""
        validators = {
            'student_id': validate_student_id,
            'name': validate_name,
            'gender': validate_gender,
            'birth_date': validate_birth_date,
            'class_name': validate_class_name,
            'enrollment_year': validate_enrollment_year
        }
        
        if field_name not in validators:
            return False, f"未知字段: {field_name}"
        
        return validators[field_name](value)
