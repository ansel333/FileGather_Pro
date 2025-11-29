"""
工具函数模块
提供字体注册、格式化、日志、文件工具等通用函数
"""

import datetime
import re
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_multilingual_fonts():
    """注册支持多语言的字体"""
    system_fonts = {
        "SimSun": "C:/Windows/Fonts/simsun.ttc",         # 宋体常规
        "SimSun-Bold": "C:/Windows/Fonts/simsunb.ttf",   # 宋体粗体
        "Microsoft YaHei": "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        "Arial": "C:/Windows/Fonts/arial.ttf"            # Arial
    }

    for font_name, font_path in system_fonts.items():
        try:
            if Path(font_path).exists():
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                print(f"成功注册字体: {font_name}")
            else:
                print(f"字体文件不存在: {font_path}")
        except Exception as e:
            print(f"注册字体 {font_name} 时出错: {str(e)}")

    if not pdfmetrics.getRegisteredFontNames():
        try:
            pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
            print("使用 ReportLab 默认字体 Vera")
        except:
            pass


def format_size(size):
    """格式化文件大小"""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size/1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size/(1024*1024):.2f} MB"
    else:
        return f"{size/(1024*1024*1024):.2f} GB"


def wrap_text(text, max_len=40):
    """将长文本自动换行，max_len为每行最大字符数"""
    if not text or len(text) <= max_len:
        return text
    lines = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    return "<br/>".join(lines)


def extract_filename_for_log(log):
    """从日志字符串中提取文件名（不含路径），如无则原样返回"""
    match = re.search(r'([A-Z]:\\[^\s]+)', log)
    if match:
        path = match.group(1)
        filename = Path(path).name
        return log.replace(path, filename)
    return log


def is_file_locked(filepath):
    """检测文件是否被占用"""
    try:
        # 尝试以追加模式打开文件
        with open(filepath, 'ab') as f:
            return False
    except IOError:
        return True
    except Exception:
        # 其他异常不视为占用
        return False


def get_file_info_dict(file_path, file_size, mod_date):
    """创建文件信息字典"""
    return {
        'path': str(file_path),
        'name': file_path.name,
        'size': file_size,
        'mod_date': mod_date.strftime("%Y-%m-%d")
    }
