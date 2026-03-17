"""
工具函数模块 - 提供排序、统计、格式化输出等纯工具函数

本模块包含所有不涉及业务逻辑的纯工具函数，包括：
- 学生列表排序
- 统计功能
- 格式化输出（表格、边框等）
"""

import os
from typing import List, Dict, Any, Optional
from collections import Counter

from utils.config import (
    BORDER_CHAR,
    BORDER_WIDTH,
    ALL_FIELDS,
    FIELD_DISPLAY_NAMES,
    FIELD_ENROLL_YEAR,
    FIELD_CLASS_NAME,
    OUTPUT_DIR,
)


def sort_students(students: List[Dict[str, Any]], sort_by: str, reverse: bool = False) -> List[Dict[str, Any]]:
    """
    对学生列表进行排序
    
    Args:
        students: 学生列表
        sort_by: 排序字段（enroll_year 或 class_name）
        reverse: 是否降序排列
        
    Returns:
        List[Dict[str, Any]]: 排序后的学生列表
    """
    if not students:
        return students
    
    valid_sort_fields = [FIELD_ENROLL_YEAR, FIELD_CLASS_NAME]
    
    if sort_by not in valid_sort_fields:
        return students
    
    return sorted(students, key=lambda x: x.get(sort_by, ""), reverse=reverse)


def count_total(students: List[Dict[str, Any]]) -> int:
    """
    统计学生总人数
    
    Args:
        students: 学生列表
        
    Returns:
        int: 学生总人数
    """
    return len(students)


def count_by_field(students: List[Dict[str, Any]], field: str) -> Dict[str, int]:
    """
    按指定字段统计人数分布
    
    Args:
        students: 学生列表
        field: 统计字段
        
    Returns:
        Dict[str, int]: 各值对应的人数
    """
    if not students:
        return {}
    
    values = [s.get(field, "未知") for s in students]
    return dict(Counter(values))


def print_border(char: str = BORDER_CHAR, width: int = BORDER_WIDTH) -> None:
    """
    打印分隔线
    
    Args:
        char: 分隔字符
        width: 分隔线宽度
    """
    print(char * width)


def print_title(title: str, char: str = BORDER_CHAR, width: int = BORDER_WIDTH) -> None:
    """
    打印带边框的标题
    
    Args:
        title: 标题文本
        char: 边框字符
        width: 边框宽度
    """
    print_border(char, width)
    padding = (width - len(title) - 2) // 2
    print(f"{char}{' ' * padding}{title}{' ' * (width - padding - len(title) - 2)}{char}")
    print_border(char, width)


def print_student_table(students: List[Dict[str, Any]]) -> None:
    """
    以表格形式打印学生信息
    
    Args:
        students: 学生列表
    """
    if not students:
        print_info("暂无学生数据")
        return
    
    col_widths = {
        "student_id": 12,
        "name": 10,
        "gender": 6,
        "birth_date": 12,
        "class_name": 14,
        "enroll_year": 10,
    }
    
    header = "|"
    for field in ALL_FIELDS:
        display_name = FIELD_DISPLAY_NAMES.get(field, field)
        width = col_widths.get(field, 10)
        header += f" {display_name:^{width}} |"
    print(header)
    
    print_border("-", len(header))
    
    for student in students:
        row = "|"
        for field in ALL_FIELDS:
            value = str(student.get(field, ""))
            width = col_widths.get(field, 10)
            if len(value) > width:
                value = value[:width - 2] + ".."
            row += f" {value:<{width}} |"
        print(row)


def print_student_detail(student: Dict[str, Any]) -> None:
    """
    打印单个学生的详细信息
    
    Args:
        student: 学生信息字典
    """
    print_border()
    for field in ALL_FIELDS:
        display_name = FIELD_DISPLAY_NAMES.get(field, field)
        value = student.get(field, "")
        print(f"  {display_name}：{value}")
    print_border()


def print_success(message: str) -> None:
    """
    打印成功消息
    
    Args:
        message: 消息内容
    """
    print(f"\n[成功] {message}\n")


def print_error(message: str) -> None:
    """
    打印错误消息
    
    Args:
        message: 消息内容
    """
    print(f"\n[错误] {message}\n")


def print_info(message: str) -> None:
    """
    打印提示消息
    
    Args:
        message: 消息内容
    """
    print(f"\n[信息] {message}\n")


def print_statistics(total: int, by_enroll_year: Dict[str, int], by_class: Dict[str, int]) -> None:
    """
    打印统计信息
    
    Args:
        total: 总人数
        by_enroll_year: 按入学年份统计
        by_class: 按班级统计
    """
    print_title("统计信息")
    print(f"\n  总人数：{total} 人\n")
    
    print("  按入学年份分布：")
    print_border("-", 30)
    for year, count in sorted(by_enroll_year.items()):
        print(f"    {year}年：{count} 人")
    
    print("\n  按班级分布：")
    print_border("-", 30)
    for class_name, count in sorted(by_class.items()):
        print(f"    {class_name}：{count} 人")
    
    print_border()


def ensure_output_dir() -> None:
    """
    确保输出目录存在
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def write_log(log_content: str, log_file: str) -> bool:
    """
    写入日志文件到输出目录
    
    Args:
        log_content: 日志内容
        log_file: 日志文件名
        
    Returns:
        bool: 是否写入成功
    """
    try:
        ensure_output_dir()
        log_path = os.path.join(OUTPUT_DIR, log_file)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_content + "\n")
        return True
    except Exception:
        return False
