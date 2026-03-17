"""
命令行解析与交互菜单模块
"""
import sys
from typing import Optional, List
from data_manager import DataManager
from core_student import Student, StudentValidator
from utils.helpers import print_table, print_separator, print_statistics
from utils.config import ALLOWED_GENDERS, FIELD_DISPLAY_NAMES


class CLIParser:
    """命令行解析器"""
    
    def __init__(self, data_manager: DataManager):
        self.dm = data_manager
    
    def run_interactive(self) -> None:
        """运行交互式菜单"""
        while True:
            self._show_menu()
            choice = input("请选择操作 [0-6]: ").strip()
            
            if choice == '0':
                print("\n感谢使用，再见！")
                break
            elif choice == '1':
                self._handle_add()
            elif choice == '2':
                self._handle_delete()
            elif choice == '3':
                self._handle_update()
            elif choice == '4':
                self._handle_search()
            elif choice == '5':
                self._handle_list()
            elif choice == '6':
                self._handle_statistics()
            else:
                print("[错误] 无效选择，请输入 0-6")
    
    def _show_menu(self) -> None:
        """显示主菜单"""
        print_separator()
        print("        学生信息管理系统")
        print_separator()
        print("  1. 添加学生")
        print("  2. 删除学生")
        print("  3. 修改学生信息")
        print("  4. 查询学生")
        print("  5. 列出所有学生")
        print("  6. 统计信息")
        print("  0. 退出系统")
        print_separator()
    
    def _handle_add(self) -> None:
        """处理添加学生"""
        print("\n--- 添加学生 ---")
        
        student_id = input("学号 (8位数字): ").strip()
        name = input("姓名: ").strip()
        gender = input(f"性别 ({'/'.join(ALLOWED_GENDERS)}): ").strip()
        birth_date = input("出生年月 (YYYY-MM): ").strip()
        class_name = input("班级 (如: 高一(3)班): ").strip()
        enrollment_year = input("入学年份 (YYYY): ").strip()
        
        valid, msg = StudentValidator.validate_all(
            student_id, name, gender, birth_date,
            class_name, enrollment_year,
            self.dm.get_existing_ids()
        )
        
        if not valid:
            print(f"[失败] {msg}")
            return
        
        student = Student(
            student_id, name, gender,
            birth_date, class_name, enrollment_year
        )
        
        success, result = self.dm.add_student(student)
        print(f"[{'成功' if success else '失败'}] {result}")
    
    def _handle_delete(self) -> None:
        """处理删除学生"""
        print("\n--- 删除学生 ---")
        student_id = input("请输入要删除的学号: ").strip()
        
        student = self.dm.get_student(student_id)
        if student:
            print(f"找到学生: {student}")
            confirm = input("确认删除? (y/n): ").strip().lower()
            if confirm == 'y':
                success, result = self.dm.delete_student(student_id)
                print(f"[{'成功' if success else '失败'}] {result}")
            else:
                print("[取消] 操作已取消")
        else:
            print(f"[失败] 学号 {student_id} 不存在")
    
    def _handle_update(self) -> None:
        """处理更新学生"""
        print("\n--- 修改学生信息 ---")
        student_id = input("请输入要修改的学号: ").strip()
        
        student = self.dm.get_student(student_id)
        if not student:
            print(f"[失败] 学号 {student_id} 不存在")
            return
        
        print(f"当前信息: {student}")
        print("请输入新值 (直接回车保持不变)")
        
        updates = {}
        fields = [
            ('name', '姓名'),
            ('gender', f"性别 ({'/'.join(ALLOWED_GENDERS)})"),
            ('birth_date', '出生年月 (YYYY-MM)'),
            ('class_name', '班级'),
            ('enrollment_year', '入学年份 (YYYY)')
        ]
        
        for field, prompt in fields:
            new_value = input(f"{prompt}: ").strip()
            if new_value:
                valid, msg = StudentValidator.validate_field(field, new_value)
                if valid:
                    updates[field] = new_value
                else:
                    print(f"[警告] {field} 校验失败: {msg}，已跳过")
        
        if updates:
            success, result = self.dm.update_student(student_id, updates)
            print(f"[{'成功' if success else '失败'}] {result}")
        else:
            print("[提示] 没有修改任何字段")
    
    def _handle_search(self) -> None:
        """处理查询学生"""
        print("\n--- 查询学生 ---")
        print("可按学号/姓名/班级查询，多个条件可组合")
        
        student_id = input("学号 (回车跳过): ").strip() or None
        name = input("姓名 (支持模糊查询，回车跳过): ").strip() or None
        class_name = input("班级 (回车跳过): ").strip() or None
        
        if not any([student_id, name, class_name]):
            print("[提示] 请至少输入一个查询条件")
            return
        
        results = self.dm.search_students(
            student_id=student_id,
            name=name,
            class_name=class_name
        )
        
        if results:
            print(f"\n找到 {len(results)} 条记录:")
            print_table(results)
        else:
            print("[结果] 未找到匹配的学生")
    
    def _handle_list(self) -> None:
        """处理列出所有学生"""
        print("\n--- 所有学生列表 ---")
        
        sort_by = input("排序方式 (1=入学年份, 2=班级, 回车=默认): ").strip()
        
        sort_field = None
        if sort_by == '1':
            sort_field = 'enrollment_year'
        elif sort_by == '2':
            sort_field = 'class_name'
        
        students = self.dm.get_all_students(sort_by=sort_field)
        
        if students:
            print(f"\n共 {len(students)} 名学生:")
            print_table(students)
        else:
            print("[提示] 暂无学生数据")
    
    def _handle_statistics(self) -> None:
        """处理统计信息"""
        print("\n--- 统计信息 ---")
        stats = self.dm.get_statistics()
        print_statistics(stats)
    
    def run_command(self) -> None:
        """运行命令行模式"""
        args = sys.argv[1:]
        
        if not args:
            self.run_interactive()
            return
        
        command = args[0].lower()
        
        if command in ['-h', '--help']:
            self._show_help()
        elif command == 'add':
            self._cmd_add(args[1:])
        elif command == 'delete':
            self._cmd_delete(args[1:])
        elif command == 'update':
            self._cmd_update(args[1:])
        elif command == 'search':
            self._cmd_search(args[1:])
        elif command == 'list':
            self._cmd_list(args[1:])
        elif command == 'stats':
            self._cmd_stats()
        else:
            print(f"[错误] 未知命令: {command}")
            self._show_help()
    
    def _show_help(self) -> None:
        """显示帮助信息"""
        print_separator()
        print("学生信息管理系统 - 命令行帮助")
        print_separator()
        print("用法: python main.py <command> [options]")
        print()
        print("命令:")
        print("  add     添加学生")
        print("  delete  删除学生")
        print("  update  更新学生信息")
        print("  search  查询学生")
        print("  list    列出所有学生")
        print("  stats   显示统计信息")
        print("  -h      显示帮助")
        print()
        print("示例:")
        print("  python main.py add --id 20240001 --name 张三 --gender 男 \\")
        print("                    --birth 2006-05 --class 高一(3)班 --year 2024")
        print("  python main.py delete --id 20240001")
        print("  python main.py search --name 张")
        print("  python main.py list --sort year")
        print_separator()
    
    def _cmd_add(self, args: List[str]) -> None:
        """命令行添加学生"""
        params = self._parse_args(args)
        
        required = ['id', 'name', 'gender', 'birth', 'class', 'year']
        for r in required:
            if r not in params:
                print(f"[错误] 缺少参数: --{r}")
                return
        
        valid, msg = StudentValidator.validate_all(
            params['id'], params['name'], params['gender'],
            params['birth'], params['class'], params['year'],
            self.dm.get_existing_ids()
        )
        
        if not valid:
            print(f"[失败] {msg}")
            return
        
        student = Student(
            params['id'], params['name'], params['gender'],
            params['birth'], params['class'], params['year']
        )
        
        success, result = self.dm.add_student(student)
        print(f"[{'成功' if success else '失败'}] {result}")
    
    def _cmd_delete(self, args: List[str]) -> None:
        """命令行删除学生"""
        params = self._parse_args(args)
        
        if 'id' not in params:
            print("[错误] 缺少参数: --id")
            return
        
        success, result = self.dm.delete_student(params['id'])
        print(f"[{'成功' if success else '失败'}] {result}")
    
    def _cmd_update(self, args: List[str]) -> None:
        """命令行更新学生"""
        params = self._parse_args(args)
        
        if 'id' not in params:
            print("[错误] 缺少参数: --id")
            return
        
        field_mapping = {
            'name': 'name',
            'gender': 'gender',
            'birth': 'birth_date',
            'class': 'class_name',
            'year': 'enrollment_year'
        }
        
        updates = {}
        for key, field in field_mapping.items():
            if key in params:
                valid, msg = StudentValidator.validate_field(field, params[key])
                if valid:
                    updates[field] = params[key]
                else:
                    print(f"[警告] {field} 校验失败: {msg}")
        
        if updates:
            success, result = self.dm.update_student(params['id'], updates)
            print(f"[{'成功' if success else '失败'}] {result}")
        else:
            print("[提示] 没有有效的更新字段")
    
    def _cmd_search(self, args: List[str]) -> None:
        """命令行查询学生"""
        params = self._parse_args(args)
        
        results = self.dm.search_students(
            student_id=params.get('id'),
            name=params.get('name'),
            class_name=params.get('class')
        )
        
        if results:
            print(f"找到 {len(results)} 条记录:")
            print_table(results)
        else:
            print("[结果] 未找到匹配的学生")
    
    def _cmd_list(self, args: List[str]) -> None:
        """命令行列出学生"""
        params = self._parse_args(args)
        
        sort_by = None
        if params.get('sort') == 'year':
            sort_by = 'enrollment_year'
        elif params.get('sort') == 'class':
            sort_by = 'class_name'
        
        students = self.dm.get_all_students(sort_by=sort_by)
        
        if students:
            print(f"共 {len(students)} 名学生:")
            print_table(students)
        else:
            print("[提示] 暂无学生数据")
    
    def _cmd_stats(self) -> None:
        """命令行统计"""
        stats = self.dm.get_statistics()
        print_statistics(stats)
    
    def _parse_args(self, args: List[str]) -> dict:
        """解析命令行参数"""
        params = {}
        i = 0
        while i < len(args):
            if args[i].startswith('--'):
                key = args[i][2:]
                if i + 1 < len(args) and not args[i + 1].startswith('--'):
                    params[key] = args[i + 1]
                    i += 2
                else:
                    params[key] = True
                    i += 1
            else:
                i += 1
        return params
