"""
工具函数模块

提供排序、统计、格式化输出等纯工具函数。
"""

from typing import List, Dict, Any
from core_student import Student


def print_separator(char: str = "-", length: int = 60) -> None:
    print(char * length)


def print_box(title: str, width: int = 50) -> None:
    print("+" + "-" * (width - 2) + "+")
    padding = (width - 4 - len(title)) // 2
    print("|" + " " * padding + title + " " * (width - 4 - padding - len(title)) + "|")
    print("+" + "-" * (width - 2) + "+")


def print_student_table(students: List[Student], page_size: int = 20) -> None:
    if not students:
        print("[提示] 无数据")
        return
    
    header = (
        f"{'学号':^12} | {'姓名':^8} | {'性别':^4} | "
        f"{'出生年月':^10} | {'班级':^12} | {'入学年份':^8}"
    )
    
    print_separator("=", 80)
    print(header)
    print_separator("=", 80)
    
    for i, student in enumerate(students, 1):
        row = (
            f"{student.student_id:^12} | {student.name:^8} | {student.gender:^4} | "
            f"{student.birth_date:^10} | {student.class_name:^12} | {student.enrollment_year:^8}"
        )
        print(row)
        
        if i % page_size == 0 and i < len(students):
            print_separator("-", 80)
            input("按 Enter 继续...")
            print_separator("-", 80)
    
    print_separator("=", 80)


def print_statistics(stats: Dict[str, Any]) -> None:
    print_separator("=", 50)
    print(f"{'统计信息':^46}")
    print_separator("=", 50)
    
    print(f"\n总人数: {stats['total']} 人")
    
    print("\n班级人数分布:")
    print_separator("-", 40)
    for class_name, count in sorted(stats['class_distribution'].items()):
        print(f"  {class_name}: {count} 人")
    
    print("\n入学年份分布:")
    print_separator("-", 40)
    for year, count in sorted(stats['year_distribution'].items(), reverse=True):
        print(f"  {year}年: {count} 人")
    
    print_separator("=", 50)


def sort_students(students: List[Student], sort_by: str = "student_id") -> List[Student]:
    sort_keys = {
        "student_id": lambda s: s.student_id,
        "name": lambda s: s.name,
        "gender": lambda s: s.gender,
        "birth_date": lambda s: s.birth_date,
        "class_name": lambda s: s.class_name,
        "enrollment_year": lambda s: s.enrollment_year,
    }
    
    if sort_by not in sort_keys:
        sort_by = "student_id"
    
    return sorted(students, key=sort_keys[sort_by])


def format_student_info(student: Student) -> str:
    return (
        f"学号: {student.student_id}\n"
        f"姓名: {student.name}\n"
        f"性别: {student.gender}\n"
        f"出生年月: {student.birth_date}\n"
        f"班级: {student.class_name}\n"
        f"入学年份: {student.enrollment_year}"
    )


def truncate_string(s: str, max_length: int = 20) -> str:
    if len(s) <= max_length:
        return s
    return s[:max_length - 3] + "..."


def count_by_field(students: List[Student], field: str) -> Dict[str, int]:
    result: Dict[str, int] = {}
    
    for student in students:
        value = getattr(student, field, "未知")
        result[value] = result.get(value, 0) + 1
    
    return result


def filter_students(
    students: List[Student],
    field: str,
    value: str,
    exact_match: bool = False
) -> List[Student]:
    results = []
    
    for student in students:
        field_value = getattr(student, field, "")
        
        if exact_match:
            if field_value == value:
                results.append(student)
        else:
            if value.lower() in field_value.lower():
                results.append(student)
    
    return results
