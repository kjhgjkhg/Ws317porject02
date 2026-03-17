"""
工具函数模块：排序、统计、格式化输出
"""
from typing import List, Dict, Optional
from collections import Counter
from core_student import Student
from utils.config import FIELD_DISPLAY_NAMES


def print_separator(char: str = '=', length: int = 50) -> None:
    """打印分隔线"""
    print(char * length)


def print_table(students: List[Student]) -> None:
    """以表格形式打印学生列表"""
    if not students:
        print("[提示] 无数据")
        return
    
    headers = ['学号', '姓名', '性别', '出生年月', '班级', '入学年份']
    col_widths = [12, 10, 6, 12, 14, 10]
    
    print_separator('-', sum(col_widths) + len(col_widths) * 3 + 1)
    
    header_line = '|'
    for i, header in enumerate(headers):
        header_line += f' {header:^{col_widths[i]}} |'
    print(header_line)
    
    print_separator('|', sum(col_widths) + len(col_widths) * 3 + 1)
    
    for student in students:
        row = '|'
        values = [
            student.student_id,
            student.name,
            student.gender,
            student.birth_date,
            student.class_name,
            student.enrollment_year
        ]
        for i, value in enumerate(values):
            row += f' {value:<{col_widths[i]}} |'
        print(row)
    
    print_separator('-', sum(col_widths) + len(col_widths) * 3 + 1)


def sort_students(students: List[Student], sort_by: str) -> List[Student]:
    """排序学生列表"""
    if not students:
        return students
    
    reverse = False
    
    if sort_by == 'enrollment_year':
        key_func = lambda s: s.enrollment_year
    elif sort_by == 'class_name':
        key_func = lambda s: s.class_name
    elif sort_by == 'student_id':
        key_func = lambda s: s.student_id
    elif sort_by == 'name':
        key_func = lambda s: s.name
    else:
        return students
    
    return sorted(students, key=key_func, reverse=reverse)


def filter_students(
    students: List[Student],
    student_id: Optional[str] = None,
    name: Optional[str] = None,
    class_name: Optional[str] = None
) -> List[Student]:
    """筛选学生列表"""
    result = students
    
    if student_id:
        result = [s for s in result if student_id in s.student_id]
    
    if name:
        result = [s for s in result if name in s.name]
    
    if class_name:
        result = [s for s in result if class_name in s.class_name]
    
    return result


def calculate_statistics(students: List[Student]) -> Dict[str, any]:
    """计算统计数据"""
    total = len(students)
    
    year_counter = Counter(s.enrollment_year for s in students)
    class_counter = Counter(s.class_name for s in students)
    gender_counter = Counter(s.gender for s in students)
    
    return {
        'total': total,
        'by_year': dict(year_counter),
        'by_class': dict(class_counter),
        'by_gender': dict(gender_counter)
    }


def print_statistics(stats: Dict[str, any]) -> None:
    """打印统计信息"""
    print_separator('=')
    print("           统计信息")
    print_separator('=')
    
    print(f"\n[总人数] {stats['total']} 人")
    
    print("\n[按入学年份分布]")
    print_separator('-', 30)
    for year, count in sorted(stats['by_year'].items(), reverse=True):
        print(f"  {year}年: {count} 人")
    
    print("\n[按班级分布]")
    print_separator('-', 30)
    for class_name, count in sorted(stats['by_class'].items()):
        print(f"  {class_name}: {count} 人")
    
    print("\n[按性别分布]")
    print_separator('-', 30)
    for gender, count in stats['by_gender'].items():
        print(f"  {gender}: {count} 人")
    
    print_separator('=')


def format_student_detail(student: Student) -> str:
    """格式化单个学生详细信息"""
    lines = [
        print_separator('='),
        "           学生详细信息",
        print_separator('='),
    ]
    
    for field, display_name in FIELD_DISPLAY_NAMES.items():
        value = getattr(student, field, '')
        lines.append(f"  {display_name}: {value}")
    
    lines.append(print_separator('='))
    
    return '\n'.join(lines)
