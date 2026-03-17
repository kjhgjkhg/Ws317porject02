"""
命令行解析模块

实现交互式菜单与命令行参数解析，协调用户操作。
"""

import sys
from typing import Optional, List
from data_manager import DataManager
from core_student import Student
from utils.helpers import (
    print_separator, print_box, print_student_table,
    print_statistics, sort_students
)


class CLIParser:
    FIELD_NAMES = {
        "1": "name",
        "2": "gender",
        "3": "birth_date",
        "4": "class_name",
        "5": "enrollment_year"
    }
    
    FIELD_LABELS = {
        "name": "姓名",
        "gender": "性别",
        "birth_date": "出生年月",
        "class_name": "班级",
        "enrollment_year": "入学年份",
        "student_id": "学号"
    }
    
    def __init__(self, data_manager: DataManager) -> None:
        self.data_manager = data_manager
    
    def interactive_mode(self) -> None:
        while True:
            self._show_main_menu()
            choice = input("请选择操作 [0-6]: ").strip()
            
            if choice == "0":
                print("\n感谢使用，再见！")
                break
            elif choice == "1":
                self._handle_add_student()
            elif choice == "2":
                self._handle_delete_student()
            elif choice == "3":
                self._handle_update_student()
            elif choice == "4":
                self._handle_search_student()
            elif choice == "5":
                self._handle_list_students()
            elif choice == "6":
                self._handle_statistics()
            else:
                print("[提示] 无效选择，请重新输入")
            
            print_separator()
    
    def _show_main_menu(self) -> None:
        print_box("主菜单")
        print("  1. 添加学生")
        print("  2. 删除学生")
        print("  3. 修改学生信息")
        print("  4. 查询学生")
        print("  5. 列出所有学生")
        print("  6. 统计信息")
        print("  0. 退出系统")
        print_separator()
    
    def _handle_add_student(self) -> None:
        print_box("添加学生")
        
        student_id = input("学号 (8位数字): ").strip()
        name = input("姓名: ").strip()
        gender = input("性别 (男/女/其他): ").strip()
        birth_date = input("出生年月 (YYYY-MM): ").strip()
        class_name = input("班级: ").strip()
        enrollment_year = input("入学年份: ").strip()
        
        student = Student(
            student_id=student_id,
            name=name,
            gender=gender,
            birth_date=birth_date,
            class_name=class_name,
            enrollment_year=enrollment_year
        )
        
        success, message = self.data_manager.add_student(student)
        print(f"\n[{'成功' if success else '失败'}] {message}")
    
    def _handle_delete_student(self) -> None:
        print_box("删除学生")
        
        student_id = input("请输入要删除的学生学号: ").strip()
        
        student = self.data_manager.get_student_by_id(student_id)
        if student:
            print(f"\n找到学生: {student}")
            confirm = input("确认删除? (y/n): ").strip().lower()
            if confirm == "y":
                success, message = self.data_manager.delete_student(student_id)
                print(f"\n[{'成功' if success else '失败'}] {message}")
            else:
                print("\n[取消] 已取消删除操作")
        else:
            print(f"\n[错误] 学号 {student_id} 不存在")
    
    def _handle_update_student(self) -> None:
        print_box("修改学生信息")
        
        student_id = input("请输入要修改的学生学号: ").strip()
        
        student = self.data_manager.get_student_by_id(student_id)
        if not student:
            print(f"\n[错误] 学号 {student_id} 不存在")
            return
        
        print(f"\n当前学生信息: {student}")
        print("\n可修改的字段:")
        print("  1. 姓名")
        print("  2. 性别")
        print("  3. 出生年月")
        print("  4. 班级")
        print("  5. 入学年份")
        
        field_choice = input("\n请选择要修改的字段 [1-5]: ").strip()
        
        if field_choice not in self.FIELD_NAMES:
            print("\n[错误] 无效选择")
            return
        
        field = self.FIELD_NAMES[field_choice]
        new_value = input(f"请输入新的{self.FIELD_LABELS[field]}: ").strip()
        
        success, message = self.data_manager.update_student(student_id, field, new_value)
        print(f"\n[{'成功' if success else '失败'}] {message}")
    
    def _handle_search_student(self) -> None:
        print_box("查询学生")
        
        print("查询方式:")
        print("  1. 按学号查询")
        print("  2. 按姓名查询")
        print("  3. 按班级查询")
        print("  4. 组合查询")
        
        choice = input("\n请选择查询方式 [1-4]: ").strip()
        
        student_id = None
        name = None
        class_name = None
        
        if choice == "1":
            student_id = input("请输入学号 (支持模糊匹配): ").strip()
        elif choice == "2":
            name = input("请输入姓名 (支持模糊匹配): ").strip()
        elif choice == "3":
            class_name = input("请输入班级 (支持模糊匹配): ").strip()
        elif choice == "4":
            student_id = input("学号 (留空跳过): ").strip() or None
            name = input("姓名 (留空跳过): ").strip() or None
            class_name = input("班级 (留空跳过): ").strip() or None
        else:
            print("\n[错误] 无效选择")
            return
        
        results = self.data_manager.search_students(
            student_id=student_id,
            name=name,
            class_name=class_name
        )
        
        if results:
            print(f"\n找到 {len(results)} 条记录:")
            print_student_table(results)
        else:
            print("\n[提示] 未找到匹配的学生")
    
    def _handle_list_students(self) -> None:
        print_box("列出所有学生")
        
        students = self.data_manager.get_all_students()
        
        if not students:
            print("\n[提示] 暂无学生数据")
            return
        
        print("\n排序方式:")
        print("  1. 按入学年份排序")
        print("  2. 按班级排序")
        print("  3. 按学号排序")
        
        choice = input("\n请选择排序方式 [1-3]: ").strip()
        
        if choice == "1":
            students = sort_students(students, "enrollment_year")
        elif choice == "2":
            students = sort_students(students, "class_name")
        elif choice == "3":
            students = sort_students(students, "student_id")
        
        print(f"\n共 {len(students)} 名学生:")
        print_student_table(students)
    
    def _handle_statistics(self) -> None:
        print_box("统计信息")
        
        stats = self.data_manager.get_statistics()
        print_statistics(stats)
    
    def parse_and_execute(self, args: List[str]) -> None:
        if not args:
            self.interactive_mode()
            return
        
        command = args[0].lower()
        
        if command in ("add", "a"):
            self._cli_add_student(args[1:])
        elif command in ("delete", "del", "d"):
            self._cli_delete_student(args[1:])
        elif command in ("update", "upd", "u"):
            self._cli_update_student(args[1:])
        elif command in ("search", "find", "s"):
            self._cli_search_student(args[1:])
        elif command in ("list", "ls", "l"):
            self._cli_list_students(args[1:])
        elif command in ("stats", "stat"):
            self._cli_statistics()
        elif command in ("help", "h", "-h", "--help"):
            self._show_help()
        else:
            print(f"[错误] 未知命令: {command}")
            self._show_help()
    
    def _cli_add_student(self, args: List[str]) -> None:
        if len(args) < 6:
            print("[错误] 用法: add <学号> <姓名> <性别> <出生年月> <班级> <入学年份>")
            return
        
        student = Student(
            student_id=args[0],
            name=args[1],
            gender=args[2],
            birth_date=args[3],
            class_name=args[4],
            enrollment_year=args[5]
        )
        
        success, message = self.data_manager.add_student(student)
        print(f"[{'成功' if success else '失败'}] {message}")
    
    def _cli_delete_student(self, args: List[str]) -> None:
        if not args:
            print("[错误] 用法: delete <学号>")
            return
        
        success, message = self.data_manager.delete_student(args[0])
        print(f"[{'成功' if success else '失败'}] {message}")
    
    def _cli_update_student(self, args: List[str]) -> None:
        if len(args) < 3:
            print("[错误] 用法: update <学号> <字段> <新值>")
            print("可用字段: name, gender, birth_date, class_name, enrollment_year")
            return
        
        success, message = self.data_manager.update_student(args[0], args[1], args[2])
        print(f"[{'成功' if success else '失败'}] {message}")
    
    def _cli_search_student(self, args: List[str]) -> None:
        student_id = None
        name = None
        class_name = None
        
        i = 0
        while i < len(args):
            if args[i] == "--id" and i + 1 < len(args):
                student_id = args[i + 1]
                i += 2
            elif args[i] == "--name" and i + 1 < len(args):
                name = args[i + 1]
                i += 2
            elif args[i] == "--class" and i + 1 < len(args):
                class_name = args[i + 1]
                i += 2
            else:
                i += 1
        
        results = self.data_manager.search_students(
            student_id=student_id,
            name=name,
            class_name=class_name
        )
        
        if results:
            print(f"找到 {len(results)} 条记录:")
            print_student_table(results)
        else:
            print("[提示] 未找到匹配的学生")
    
    def _cli_list_students(self, args: List[str]) -> None:
        students = self.data_manager.get_all_students()
        
        sort_by = "student_id"
        if args and args[0] in ("--year", "-y"):
            sort_by = "enrollment_year"
        elif args and args[0] in ("--class", "-c"):
            sort_by = "class_name"
        
        students = sort_students(students, sort_by)
        print(f"共 {len(students)} 名学生:")
        print_student_table(students)
    
    def _cli_statistics(self) -> None:
        stats = self.data_manager.get_statistics()
        print_statistics(stats)
    
    def _show_help(self) -> None:
        print_box("命令帮助")
        print("交互模式: python main.py")
        print("命令行模式: python main.py <命令> [参数]")
        print()
        print("可用命令:")
        print("  add <学号> <姓名> <性别> <出生年月> <班级> <入学年份>")
        print("      添加新学生")
        print()
        print("  delete <学号>")
        print("      删除指定学生")
        print()
        print("  update <学号> <字段> <新值>")
        print("      更新学生信息")
        print()
        print("  search [--id 学号] [--name 姓名] [--class 班级]")
        print("      查询学生")
        print()
        print("  list [--year|--class]")
        print("      列出所有学生")
        print()
        print("  stats")
        print("      显示统计信息")
        print_separator()
