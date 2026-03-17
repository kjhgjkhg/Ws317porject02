"""
数据管理模块
负责JSON读写、数据加载/保存、增删改查核心逻辑
"""
import json
import os
from typing import List, Dict, Optional
from core_student import Student
from utils.config import DATA_DIR, STUDENT_FILE, CONFIG_FILE
from utils.helpers import sort_students, filter_students, calculate_statistics


class DataManager:
    """数据管理器"""
    
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self._ensure_data_file()
        self.load_data()
    
    def _ensure_data_file(self) -> None:
        """确保数据文件存在"""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        
        if not os.path.exists(STUDENT_FILE):
            self._save_to_file({})
    
    def _save_to_file(self, data: Dict[str, Dict]) -> None:
        """保存数据到JSON文件"""
        try:
            with open(STUDENT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise IOError(f"保存文件失败: {e}")
    
    def _load_from_file(self) -> Dict[str, Dict]:
        """从JSON文件加载数据"""
        try:
            if not os.path.exists(STUDENT_FILE):
                return {}
            
            with open(STUDENT_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON解析失败: {e}")
        except IOError as e:
            raise IOError(f"读取文件失败: {e}")
    
    def load_data(self) -> None:
        """加载数据到内存"""
        try:
            data = self._load_from_file()
            self.students = {
                sid: Student.from_dict(sdata)
                for sid, sdata in data.items()
            }
        except Exception as e:
            print(f"[警告] 加载数据失败: {e}")
            self.students = {}
    
    def save_data(self) -> None:
        """保存内存数据到文件"""
        data = {
            sid: student.to_dict()
            for sid, student in self.students.items()
        }
        self._save_to_file(data)
    
    def add_student(self, student: Student) -> tuple[bool, str]:
        """添加学生"""
        if student.student_id in self.students:
            return False, f"学号 {student.student_id} 已存在"
        
        self.students[student.student_id] = student
        self.save_data()
        return True, f"成功添加学生: {student.name} ({student.student_id})"
    
    def delete_student(self, student_id: str) -> tuple[bool, str]:
        """删除学生"""
        if student_id not in self.students:
            return False, f"学号 {student_id} 不存在"
        
        name = self.students[student_id].name
        del self.students[student_id]
        self.save_data()
        return True, f"成功删除学生: {name} ({student_id})"
    
    def update_student(self, student_id: str, updates: Dict[str, str]) -> tuple[bool, str]:
        """更新学生信息"""
        if student_id not in self.students:
            return False, f"学号 {student_id} 不存在"
        
        student = self.students[student_id]
        
        for field, value in updates.items():
            if hasattr(student, field):
                setattr(student, field, value)
        
        self.save_data()
        return True, f"成功更新学生信息: {student.name} ({student_id})"
    
    def get_student(self, student_id: str) -> Optional[Student]:
        """根据学号获取学生"""
        return self.students.get(student_id)
    
    def search_students(
        self,
        student_id: Optional[str] = None,
        name: Optional[str] = None,
        class_name: Optional[str] = None
    ) -> List[Student]:
        """搜索学生"""
        return filter_students(
            list(self.students.values()),
            student_id=student_id,
            name=name,
            class_name=class_name
        )
    
    def get_all_students(self, sort_by: Optional[str] = None) -> List[Student]:
        """获取所有学生"""
        students = list(self.students.values())
        if sort_by:
            students = sort_students(students, sort_by)
        return students
    
    def get_statistics(self) -> Dict[str, any]:
        """获取统计数据"""
        return calculate_statistics(list(self.students.values()))
    
    def get_existing_ids(self) -> set:
        """获取所有已存在的学号"""
        return set(self.students.keys())
