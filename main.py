"""
学生信息管理系统 - 主入口模块

本模块是程序的唯一入口，负责：
- 初始化系统组件
- 运行主循环
- 分发用户命令

使用方法：
    python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Optional, List

from data_manager import DataManager
from cli_parser import CLIParser
from core_student import Student
from utils.config import (
    FIELD_STUDENT_ID,
    FIELD_NAME,
    FIELD_CLASS_NAME,
    FIELD_ENROLL_YEAR,
)
from utils.helpers import (
    print_title,
    print_success,
    print_error,
    print_info,
    print_student_table,
    print_student_detail,
    print_statistics,
    print_border,
)


class StudentManagementSystem:
    """
    学生信息管理系统主类
    
    整合数据管理器和命令行解析器，实现完整的系统功能
    """
    
    def __init__(self) -> None:
        """
        初始化系统
        """
        self._data_manager = DataManager()
        self._cli = CLIParser()
    
    def run(self) -> None:
        """
        运行系统主循环
        """
        self._cli.show_welcome()
        
        while self._cli.is_running():
            try:
                self._cli.show_main_menu()
                choice = self._cli.get_choice()
                self._handle_main_choice(choice)
            except KeyboardInterrupt:
                print()
                print_info("检测到中断信号")
                self._cli.stop()
            except Exception as e:
                print_error(f"系统错误：{str(e)}")
        
        self._cli.show_goodbye()
    
    def _handle_main_choice(self, choice: str) -> None:
        """
        处理主菜单选择
        
        Args:
            choice: 用户选择
        """
        handlers = {
            "1": self._handle_add_student,
            "2": self._handle_delete_student,
            "3": self._handle_update_student,
            "4": self._handle_search_student,
            "5": self._handle_list_students,
            "6": self._handle_statistics,
            "0": self._handle_exit,
        }
        
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print_error("无效选择，请重新输入")
    
    def _handle_add_student(self) -> None:
        """
        处理添加学生
        """
        print_title("添加学生")
        
        student_data = self._cli.get_student_info()
        if student_data is None:
            return
        
        student_id = student_data[FIELD_STUDENT_ID]
        
        if self._data_manager.student_exists(student_id):
            print_error(f"学号 {student_id} 已存在")
            return
        
        success, message = self._data_manager.add_student(
            student_id=student_data[FIELD_STUDENT_ID],
            name=student_data[FIELD_NAME],
            gender=student_data["gender"],
            birth_date=student_data["birth_date"],
            class_name=student_data[FIELD_CLASS_NAME],
            enroll_year=student_data[FIELD_ENROLL_YEAR],
        )
        
        if success:
            print_success(message)
        else:
            print_error(message)
    
    def _handle_delete_student(self) -> None:
        """
        处理删除学生
        """
        print_title("删除学生")
        
        student_id = self._cli.get_student_id()
        if student_id is None:
            return
        
        student = self._data_manager.get_student_by_id(student_id)
        if student is None:
            print_error(f"学号 {student_id} 不存在")
            return
        print_info("找到以下学生：")
        print_student_detail(student.to_dict())
        
        if self._cli.confirm("确认删除该学生？"):
            success, message = self._data_manager.delete_student(student_id)
            if success:
                print_success(message)
            else:
                print_error(message)
        else:
            print_info("已取消删除")
    
    def _handle_update_student(self) -> None:
        """
        处理修改学生信息
        """
        print_title("修改学生信息")
        
        student_id = self._cli.get_student_id()
        if student_id is None:
            return
        
        student = self._data_manager.get_student_by_id(student_id)
        if student is None:
            print_error(f"学号 {student_id} 不存在")
            return
        
        print_info("当前学生信息：")
        print_student_detail(student.to_dict())
        
        field = self._cli.get_field_choice()
        if field is None:
            return
        
        new_value = self._cli.get_new_value(field)
        if new_value is None:
            return
        
        success, message = self._data_manager.update_student(student_id, field, new_value)
        if success:
            print_success(message)
            print_info("更新后的信息：")
            updated_student = self._data_manager.get_student_by_id(student_id)
            if updated_student:
                print_student_detail(updated_student.to_dict())
        else:
            print_error(message)
    
    def _handle_search_student(self) -> None:
        """
        处理查询学生
        """
        self._cli.show_search_menu()
        choice = self._cli.get_choice()
        
        if choice == "0":
            return
        elif choice == "1":
            self._search_by_id()
        elif choice == "2":
            self._search_by_name()
        elif choice == "3":
            self._search_by_class()
        else:
            print_error("无效选择")
    
    def _search_by_id(self) -> None:
        """
        按学号查询
        """
        student_id = self._cli.get_student_id()
        if student_id is None:
            return
        
        student = self._data_manager.get_student_by_id(student_id)
        if student:
            print_success("查询成功")
            print_student_detail(student.to_dict())
        else:
            print_error(f"学号 {student_id} 不存在")
    
    def _search_by_name(self) -> None:
        """
        按姓名查询
        """
        name = self._cli.get_input("请输入姓名关键字")
        if not name:
            return
        
        students = self._data_manager.search_by_name(name)
        if students:
            print_success(f"找到 {len(students)} 名学生")
            print_student_table([s.to_dict() for s in students])
        else:
            print_error(f"未找到姓名包含「{name}」的学生")
    
    def _search_by_class(self) -> None:
        """
        按班级查询
        """
        class_name = self._cli.get_input("请输入班级名称")
        if not class_name:
            return
        
        students = self._data_manager.search_by_class(class_name)
        if students:
            print_success(f"找到 {len(students)} 名学生")
            print_student_table([s.to_dict() for s in students])
        else:
            print_error(f"未找到班级「{class_name}」的学生")
    
    def _handle_list_students(self) -> None:
        """
        处理列出所有学生
        """
        self._cli.show_list_menu()
        choice = self._cli.get_choice()
        
        sort_options = {
            "1": (FIELD_ENROLL_YEAR, False),
            "2": (FIELD_ENROLL_YEAR, True),
            "3": (FIELD_CLASS_NAME, False),
            "4": (FIELD_CLASS_NAME, True),
        }
        
        if choice == "0":
            return
        
        if choice in sort_options:
            sort_by, reverse = sort_options[choice]
            students = self._data_manager.get_students_sorted(sort_by, reverse)
            
            if students:
                print_success(f"共 {len(students)} 名学生")
                print_student_table([s.to_dict() for s in students])
            else:
                print_info("暂无学生数据")
        else:
            print_error("无效选择")
    
    def _handle_statistics(self) -> None:
        """
        处理统计信息
        """
        stats = self._data_manager.get_statistics()
        print_statistics(
            total=stats["total"],
            by_enroll_year=stats["by_enroll_year"],
            by_class=stats["by_class"],
        )
    
    def _handle_exit(self) -> None:
        """
        处理退出
        """
        self._cli.stop()


def main() -> None:
    """
    程序入口函数
    """
    try:
        system = StudentManagementSystem()
        system.run()
    except Exception as e:
        print(f"\n[致命错误] 程序异常退出：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
