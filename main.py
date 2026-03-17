"""
学生信息管理系统 - 主入口模块

负责命令行参数解析与主程序循环，协调各模块完成用户操作。
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Optional, List
from cli_parser import CLIParser
from data_manager import DataManager
from utils.config import DATA_DIR, OUTPUT_DIR, DATA_FILE
from utils.helpers import print_separator, print_box


def ensure_directories() -> None:
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def main() -> None:
    ensure_directories()
    
    data_manager = DataManager()
    cli_parser = CLIParser(data_manager)
    
    print_box("学生信息管理系统 v1.0")
    print_separator()
    
    if len(sys.argv) > 1:
        cli_parser.parse_and_execute(sys.argv[1:])
    else:
        cli_parser.interactive_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已退出。")
        sys.exit(0)
    except Exception as e:
        print(f"\n[错误] 程序发生异常: {e}")
        sys.exit(1)
