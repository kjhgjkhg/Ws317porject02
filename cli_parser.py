"""
命令行解析模块 - 提供交互式菜单和用户输入处理

本模块包含：
- 交互式菜单显示
- 用户输入处理
- 命令分发
"""

from typing import Optional, List, Callable, Any

from utils.config import (
    ALL_FIELDS,
    FIELD_DISPLAY_NAMES,
    FIELD_STUDENT_ID,
    FIELD_NAME,
    FIELD_CLASS_NAME,
    FIELD_ENROLL_YEAR,
    FIELD_GENDER,
    FIELD_BIRTH_DATE,
)
from utils.helpers import (
    print_title,
    print_border,
    print_success,
    print_error,
    print_info,
    print_student_table,
    print_student_detail,
    print_statistics,
)
from utils.validators import (
    validate_student_id,
    validate_field,
)


class CLIParser:
    """
    命令行解析器类
    
    提供交互式菜单和用户输入处理功能
    """
    
    def __init__(self) -> None:
        """
        初始化命令行解析器
        """
        self._running: bool = True
    
    def show_main_menu(self) -> None:
        """
        显示主菜单
        """
        print_title("学生信息管理系统")
        print("  1. 添加学生")
        print("  2. 删除学生")
        print("  3. 修改学生信息")
        print("  4. 查询学生")
        print("  5. 列出所有学生")
        print("  6. 统计信息")
        print("  0. 退出系统")
        print_border()
    
    def show_search_menu(self) -> None:
        """
        显示查询子菜单
        """
        print_title("查询学生")
        print("  1. 按学号查询")
        print("  2. 按姓名查询")
        print("  3. 按班级查询")
        print("  0. 返回主菜单")
        print_border()
    
    def show_list_menu(self) -> None:
        """
        显示列表子菜单
        """
        print_title("列出学生")
        print("  1. 按入学年份升序")
        print("  2. 按入学年份降序")
        print("  3. 按班级升序")
        print("  4. 按班级降序")
        print("  0. 返回主菜单")
        print_border()
    
    def get_input(self, prompt: str) -> str:
        """
        获取用户输入
        
        Args:
            prompt: 提示信息
            
        Returns:
            str: 用户输入（已去除首尾空格）
        """
        try:
            return input(f"  {prompt}：").strip()
        except EOFError:
            return ""
        except KeyboardInterrupt:
            print()
            return ""
    
    def get_choice(self, prompt: str = "请选择") -> str:
        """
        获取用户选择
        
        Args:
            prompt: 提示信息
            
        Returns:
            str: 用户选择
        """
        return self.get_input(prompt)
    
    def get_student_info(self) -> Optional[dict]:
        """
        获取学生完整信息输入
        
        Returns:
            Optional[dict]: 学生信息字典或None（取消输入时）
        """
        print_info("请输入学生信息（输入 q 取消）")
        
        fields_prompts = [
            (FIELD_STUDENT_ID, "学号（8位数字）"),
            (FIELD_NAME, "姓名"),
            (FIELD_GENDER, "性别（男/女/其他）"),
            (FIELD_BIRTH_DATE, "出生年月（YYYY-MM）"),
            (FIELD_CLASS_NAME, "班级（如：高一（3）班）"),
            (FIELD_ENROLL_YEAR, "入学年份"),
        ]
        
        student_data = {}
        
        for field, prompt in fields_prompts:
            while True:
                value = self.get_input(prompt)
                
                if value.lower() == "q":
                    print_info("已取消操作")
                    return None
                
                is_valid, error_msg = validate_field(field, value)
                if is_valid:
                    student_data[field] = value
                    break
                else:
                    print_error(error_msg)
        
        return student_data
    
    def get_student_id(self, prompt: str = "请输入学号") -> Optional[str]:
        """
        获取并验证学号输入
        
        Args:
            prompt: 提示信息
            
        Returns:
            Optional[str]: 学号或None（取消输入时）
        """
        while True:
            student_id = self.get_input(f"{prompt}（输入 q 取消）")
            
            if student_id.lower() == "q":
                return None
            
            is_valid, error_msg = validate_student_id(student_id)
            if is_valid:
                return student_id
            
            print_error(error_msg)
    
    def get_field_choice(self) -> Optional[str]:
        """
        获取要修改的字段选择
        
        Returns:
            Optional[str]: 字段名或None
        """
        print_info("请选择要修改的字段")
        
        editable_fields = [
            FIELD_NAME,
            FIELD_GENDER,
            FIELD_BIRTH_DATE,
            FIELD_CLASS_NAME,
            FIELD_ENROLL_YEAR,
        ]
        
        for i, field in enumerate(editable_fields, 1):
            display_name = FIELD_DISPLAY_NAMES.get(field, field)
            print(f"  {i}. {display_name}")
        print("  0. 取消")
        print_border()
        
        choice = self.get_choice()
        
        if choice == "0" or choice.lower() == "q":
            return None
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(editable_fields):
                return editable_fields[index]
        except ValueError:
            pass
        
        print_error("无效选择")
        return None
    
    def get_new_value(self, field: str) -> Optional[str]:
        """
        获取字段的新值
        
        Args:
            field: 字段名
            
        Returns:
            Optional[str]: 新值或None
        """
        display_name = FIELD_DISPLAY_NAMES.get(field, field)
        
        while True:
            value = self.get_input(f"请输入新的{display_name}（输入 q 取消）")
            
            if value.lower() == "q":
                return None
            
            is_valid, error_msg = validate_field(field, value)
            if is_valid:
                return value
            
            print_error(error_msg)
    
    def confirm(self, prompt: str) -> bool:
        """
        确认操作
        
        Args:
            prompt: 提示信息
            
        Returns:
            bool: 是否确认
        """
        while True:
            choice = self.get_input(f"{prompt}（y/n）")
            if choice.lower() in ["y", "yes", "是"]:
                return True
            elif choice.lower() in ["n", "no", "否"]:
                return False
    
    def pause(self) -> None:
        """
        暂停等待用户按键
        """
        self.get_input("按回车键继续...")
    
    def is_running(self) -> bool:
        """
        检查是否继续运行
        
        Returns:
            bool: 是否继续运行
        """
        return self._running
    
    def stop(self) -> None:
        """
        停止运行
        """
        self._running = False
    
    def show_welcome(self) -> None:
        """
        显示欢迎信息
        """
        print_title("欢迎使用学生信息管理系统")
    
    def show_goodbye(self) -> None:
        """
        显示告别信息
        """
        print_title("感谢使用，再见！")
