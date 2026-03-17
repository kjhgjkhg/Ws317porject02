"""
学生信息管理系统 - 主入口模块
负责命令行解析与主循环
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli_parser import CLIParser
from data_manager import DataManager
from utils.config import DATA_DIR, OUTPUT_DIR, STUDENT_FILE


def ensure_directories() -> None:
    """确保必要的目录存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def main() -> None:
    """程序主入口"""
    ensure_directories()
    
    data_manager = DataManager()
    cli_parser = CLIParser(data_manager)
    
    if len(sys.argv) == 1:
        cli_parser.run_interactive()
    else:
        cli_parser.run_command()


if __name__ == "__main__":
    main()
