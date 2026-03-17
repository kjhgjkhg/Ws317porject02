"""
数据管理模块

负责JSON文件的读写、数据加载/保存、学生信息的增删改查核心逻辑。
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from core_student import Student, StudentValidator
from utils.config import DATA_DIR, DATA_FILE, CONFIG_FILE
from utils.helpers import print_separator


class DataManager:
    def __init__(self) -> None:
        self._students: Dict[str, Student] = {}
        self._ensure_data_file()
        self._load_data()
    
    def _ensure_data_file(self) -> None:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        
        if not os.path.exists(DATA_FILE):
            self._save_to_file()
    
    def _load_data(self) -> None:
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "students" in data:
                        for item in data["students"]:
                            if isinstance(item, dict) and "student_id" in item:
                                student = Student.from_dict(item)
                                self._students[student.student_id] = student
        except json.JSONDecodeError:
            self._students = {}
        except Exception:
            self._students = {}
    
    def _save_to_file(self) -> bool:
        try:
            data = {
                "students": [s.to_dict() for s in self._students.values()]
            }
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[错误] 保存数据失败: {e}")
            return False
    
    def get_all_students(self) -> List[Student]:
        return list(self._students.values())
    
    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        return self._students.get(student_id)
    
    def get_existing_ids(self) -> set:
        return set(self._students.keys())
    
    def add_student(self, student: Student) -> Tuple[bool, str]:
        existing_ids = self.get_existing_ids()
        valid, errors = StudentValidator.validate_all(student, existing_ids)
        
        if not valid:
            return False, "; ".join(errors)
        
        if student.student_id in self._students:
            return False, f"学号 {student.student_id} 已存在"
        
        self._students[student.student_id] = student
        if self._save_to_file():
            return True, f"成功添加学生: {student.name} ({student.student_id})"
        else:
            del self._students[student.student_id]
            return False, "添加失败：数据保存错误"
    
    def delete_student(self, student_id: str) -> Tuple[bool, str]:
        if student_id not in self._students:
            return False, f"学号 {student_id} 不存在"
        
        student = self._students[student_id]
        del self._students[student_id]
        
        if self._save_to_file():
            return True, f"成功删除学生: {student.name} ({student_id})"
        else:
            self._students[student_id] = student
            return False, "删除失败：数据保存错误"
    
    def update_student(self, student_id: str, field: str, new_value: str) -> Tuple[bool, str]:
        if student_id not in self._students:
            return False, f"学号 {student_id} 不存在"
        
        student = self._students[student_id]
        old_value = getattr(student, field, "")
        
        field_validators = {
            "name": StudentValidator.validate_name,
            "gender": StudentValidator.validate_gender,
            "birth_date": StudentValidator.validate_birth_date,
            "class_name": StudentValidator.validate_class_name,
            "enrollment_year": StudentValidator.validate_enrollment_year,
        }
        
        if field == "student_id":
            if not new_value.isdigit() or len(new_value) != 8:
                return False, "学号必须为8位纯数字"
            if new_value != student_id and new_value in self._students:
                return False, f"学号 {new_value} 已存在"
        
        if field in field_validators:
            valid, msg = field_validators[field](new_value)
            if not valid:
                return False, msg
        
        student.update(field, new_value)
        
        if field == "student_id" and new_value != student_id:
            del self._students[student_id]
            self._students[new_value] = student
        
        if self._save_to_file():
            return True, f"成功更新字段 '{field}': {old_value} -> {new_value}"
        else:
            student.update(field, old_value)
            if field == "student_id" and new_value != student_id:
                del self._students[new_value]
                self._students[student_id] = student
            return False, "更新失败：数据保存错误"
    
    def search_students(
        self,
        student_id: Optional[str] = None,
        name: Optional[str] = None,
        class_name: Optional[str] = None
    ) -> List[Student]:
        results = []
        
        for student in self._students.values():
            match = True
            
            if student_id and student_id not in student.student_id:
                match = False
            if name and name not in student.name:
                match = False
            if class_name and class_name not in student.class_name:
                match = False
            
            if match:
                results.append(student)
        
        return results
    
    def get_statistics(self) -> Dict:
        students = self.get_all_students()
        
        class_distribution: Dict[str, int] = {}
        year_distribution: Dict[str, int] = {}
        
        for student in students:
            class_name = student.class_name
            enrollment_year = student.enrollment_year
            
            class_distribution[class_name] = class_distribution.get(class_name, 0) + 1
            year_distribution[enrollment_year] = year_distribution.get(enrollment_year, 0) + 1
        
        return {
            "total": len(students),
            "class_distribution": class_distribution,
            "year_distribution": year_distribution
        }
