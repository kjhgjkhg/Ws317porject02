"""
学生数据类与业务规则校验模块

定义 Student 数据类及学生信息的业务规则校验逻辑。
"""

from typing import Dict, Any, Optional
from datetime import datetime


class Student:
    VALID_GENDERS = ("男", "女", "其他")
    
    def __init__(
        self,
        student_id: str,
        name: str,
        gender: str,
        birth_date: str,
        class_name: str,
        enrollment_year: str
    ) -> None:
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.birth_date = birth_date
        self.class_name = class_name
        self.enrollment_year = enrollment_year
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "gender": self.gender,
            "birth_date": self.birth_date,
            "class_name": self.class_name,
            "enrollment_year": self.enrollment_year
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Student":
        return cls(
            student_id=data.get("student_id", ""),
            name=data.get("name", ""),
            gender=data.get("gender", ""),
            birth_date=data.get("birth_date", ""),
            class_name=data.get("class_name", ""),
            enrollment_year=data.get("enrollment_year", "")
        )
    
    def __str__(self) -> str:
        return (
            f"学号: {self.student_id} | 姓名: {self.name} | "
            f"性别: {self.gender} | 出生年月: {self.birth_date} | "
            f"班级: {self.class_name} | 入学年份: {self.enrollment_year}"
        )
    
    def update(self, field: str, value: str) -> bool:
        field_mapping = {
            "student_id": "student_id",
            "name": "name",
            "gender": "gender",
            "birth_date": "birth_date",
            "class_name": "class_name",
            "enrollment_year": "enrollment_year"
        }
        
        if field in field_mapping:
            setattr(self, field_mapping[field], value)
            return True
        return False


class StudentValidator:
    @staticmethod
    def validate_student_id(student_id: str, existing_ids: Optional[set] = None) -> tuple:
        if not student_id:
            return False, "学号不能为空"
        if not student_id.isdigit():
            return False, "学号必须为纯数字"
        if len(student_id) != 8:
            return False, "学号必须为8位数字"
        if existing_ids and student_id in existing_ids:
            return False, f"学号 {student_id} 已存在，不可重复"
        return True, ""
    
    @staticmethod
    def validate_name(name: str) -> tuple:
        if not name or not name.strip():
            return False, "姓名不能为空"
        name = name.strip()
        if len(name) > 20:
            return False, "姓名最多20个字符"
        return True, ""
    
    @staticmethod
    def validate_gender(gender: str) -> tuple:
        if gender not in Student.VALID_GENDERS:
            return False, f"性别只允许: {', '.join(Student.VALID_GENDERS)}"
        return True, ""
    
    @staticmethod
    def validate_birth_date(birth_date: str) -> tuple:
        if not birth_date:
            return False, "出生年月不能为空"
        try:
            datetime.strptime(birth_date, "%Y-%m")
            return True, ""
        except ValueError:
            return False, "出生年月格式错误，应为 YYYY-MM"
    
    @staticmethod
    def validate_class_name(class_name: str) -> tuple:
        if not class_name or not class_name.strip():
            return False, "班级不能为空"
        return True, ""
    
    @staticmethod
    def validate_enrollment_year(enrollment_year: str) -> tuple:
        if not enrollment_year:
            return False, "入学年份不能为空"
        if not enrollment_year.isdigit():
            return False, "入学年份必须为数字"
        year = int(enrollment_year)
        current_year = datetime.now().year
        if year < 1900 or year > current_year + 1:
            return False, f"入学年份应在 1900-{current_year + 1} 之间"
        return True, ""
    
    @classmethod
    def validate_all(cls, student: Student, existing_ids: Optional[set] = None, 
                     skip_id_check: bool = False) -> tuple:
        errors = []
        
        if not skip_id_check:
            valid, msg = cls.validate_student_id(student.student_id, existing_ids)
            if not valid:
                errors.append(msg)
        
        valid, msg = cls.validate_name(student.name)
        if not valid:
            errors.append(msg)
        
        valid, msg = cls.validate_gender(student.gender)
        if not valid:
            errors.append(msg)
        
        valid, msg = cls.validate_birth_date(student.birth_date)
        if not valid:
            errors.append(msg)
        
        valid, msg = cls.validate_class_name(student.class_name)
        if not valid:
            errors.append(msg)
        
        valid, msg = cls.validate_enrollment_year(student.enrollment_year)
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, errors
