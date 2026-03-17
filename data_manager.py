"""
数据管理模块 - 负责JSON读写、数据加载/保存、增删改查核心逻辑

本模块包含：
- 数据加载与保存
- 学生信息的增删改查操作
- 数据持久化管理
"""

import json
import os
from typing import Dict, Any, List, Optional, Tuple

from utils.config import (
    DATA_DIR,
    DATA_FILE,
    CONFIG_FILE,
    FIELD_STUDENT_ID,
    FIELD_NAME,
    FIELD_CLASS_NAME,
    FIELD_ENROLL_YEAR,
)
from core_student import Student, create_student, validate_student_data


class DataManager:
    """
    数据管理器类
    
    负责学生数据的加载、保存、增删改查等操作
    """
    
    def __init__(self) -> None:
        """
        初始化数据管理器
        """
        self._students: Dict[str, Student] = {}
        self._ensure_data_dir()
        self.load_data()
    
    def _ensure_data_dir(self) -> None:
        """
        确保数据目录存在
        """
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
    
    def _ensure_data_file(self) -> None:
        """
        确保数据文件存在
        """
        if not os.path.exists(DATA_FILE):
            self._save_to_file({})
    
    def load_data(self) -> bool:
        """
        从JSON文件加载学生数据
        
        Returns:
            bool: 是否加载成功
        """
        try:
            self._ensure_data_file()
            
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not isinstance(data, dict):
                data = {}
            
            self._students = {}
            for student_id, student_data in data.items():
                if isinstance(student_data, dict):
                    is_valid, _ = validate_student_data(student_data)
                    if is_valid:
                        self._students[student_id] = Student.from_dict(student_data)
            
            return True
            
        except json.JSONDecodeError:
            self._students = {}
            return True
        except Exception:
            self._students = {}
            return False
    
    def _save_to_file(self, data: Dict[str, Any]) -> bool:
        """
        将数据保存到JSON文件
        
        Args:
            data: 要保存的数据字典
            
        Returns:
            bool: 是否保存成功
        """
        try:
            self._ensure_data_dir()
            
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def save_data(self) -> bool:
        """
        保存所有学生数据到文件
        
        Returns:
            bool: 是否保存成功
        """
        data = {
            student_id: student.to_dict()
            for student_id, student in self._students.items()
        }
        return self._save_to_file(data)
    
    def add_student(
        self,
        student_id: str,
        name: str,
        gender: str,
        birth_date: str,
        class_name: str,
        enroll_year: str
    ) -> Tuple[bool, str]:
        """
        添加学生
        
        Args:
            student_id: 学号
            name: 姓名
            gender: 性别
            birth_date: 出生年月
            class_name: 班级名称
            enroll_year: 入学年份
            
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        if student_id in self._students:
            return False, f"学号 {student_id} 已存在，不能重复添加"
        
        student, error_msg = create_student(
            student_id, name, gender, birth_date, class_name, enroll_year
        )
        
        if student is None:
            return False, error_msg
        
        self._students[student_id] = student
        self.save_data()
        
        return True, f"学生 {name} 添加成功"
    
    def delete_student(self, student_id: str) -> Tuple[bool, str]:
        """
        根据学号删除学生
        
        Args:
            student_id: 学号
            
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        if student_id not in self._students:
            return False, f"学号 {student_id} 不存在"
        
        student_name = self._students[student_id].name
        del self._students[student_id]
        self.save_data()
        
        return True, f"学生 {student_name} 删除成功"
    
    def update_student(self, student_id: str, field: str, value: str) -> Tuple[bool, str]:
        """
        更新学生信息
        
        Args:
            student_id: 学号
            field: 要更新的字段名
            value: 新值
            
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        if student_id not in self._students:
            return False, f"学号 {student_id} 不存在"
        
        if field == FIELD_STUDENT_ID:
            return False, "学号不允许修改"
        
        student = self._students[student_id]
        is_valid, error_msg = student.update_field(field, value)
        
        if not is_valid:
            return False, error_msg
        
        self.save_data()
        
        return True, f"学生信息更新成功"
    
    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """
        根据学号获取学生
        
        Args:
            student_id: 学号
            
        Returns:
            Optional[Student]: 学生对象或None
        """
        return self._students.get(student_id)
    
    def search_by_name(self, name: str) -> List[Student]:
        """
        根据姓名模糊搜索学生
        
        Args:
            name: 姓名关键字
            
        Returns:
            List[Student]: 匹配的学生列表
        """
        name = name.strip().lower()
        return [
            student for student in self._students.values()
            if name in student.name.lower()
        ]
    
    def search_by_class(self, class_name: str) -> List[Student]:
        """
        根据班级搜索学生
        
        Args:
            class_name: 班级名称
            
        Returns:
            List[Student]: 匹配的学生列表
        """
        class_name = class_name.strip()
        return [
            student for student in self._students.values()
            if class_name in student.class_name
        ]
    
    def get_all_students(self) -> List[Student]:
        """
        获取所有学生
        
        Returns:
            List[Student]: 所有学生列表
        """
        return list(self._students.values())
    
    def get_students_sorted(self, sort_by: str, reverse: bool = False) -> List[Student]:
        """
        获取排序后的学生列表
        
        Args:
            sort_by: 排序字段
            reverse: 是否降序
            
        Returns:
            List[Student]: 排序后的学生列表
        """
        students = self.get_all_students()
        
        if sort_by == FIELD_ENROLL_YEAR:
            return sorted(students, key=lambda s: s.enroll_year, reverse=reverse)
        elif sort_by == FIELD_CLASS_NAME:
            return sorted(students, key=lambda s: s.class_name, reverse=reverse)
        
        return students
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            Dict[str, Any]: 包含总人数、按年级/班级分布的统计信息
        """
        students = self.get_all_students()
        
        total = len(students)
        
        by_enroll_year: Dict[str, int] = {}
        by_class: Dict[str, int] = {}
        
        for student in students:
            year = student.enroll_year
            by_enroll_year[year] = by_enroll_year.get(year, 0) + 1
            
            cls = student.class_name
            by_class[cls] = by_class.get(cls, 0) + 1
        
        return {
            "total": total,
            "by_enroll_year": by_enroll_year,
            "by_class": by_class,
        }
    
    def student_exists(self, student_id: str) -> bool:
        """
        检查学号是否已存在
        
        Args:
            student_id: 学号
            
        Returns:
            bool: 是否存在
        """
        return student_id in self._students
