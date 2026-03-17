"""
常量配置模块
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'source_data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_build')

STUDENT_FILE = os.path.join(DATA_DIR, 'students.json')
CONFIG_FILE = os.path.join(DATA_DIR, '.do_not_touch.cfg')

ALLOWED_GENDERS = ['男', '女', '其他']

FIELD_NAMES = ['student_id', 'name', 'gender', 'birth_date', 'class_name', 'enrollment_year']

FIELD_DISPLAY_NAMES = {
    'student_id': '学号',
    'name': '姓名',
    'gender': '性别',
    'birth_date': '出生年月',
    'class_name': '班级',
    'enrollment_year': '入学年份'
}

CLASS_PATTERN = r'^[高低初一二三四五六七八九十]+[（(][一二三四五六七八九十\d]+[）)]班$'

STUDENT_ID_LENGTH = 8
NAME_MAX_LENGTH = 20
