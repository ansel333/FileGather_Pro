"""
测试精确查找功能的单元测试
"""

import sys
import os

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.search_logic import exact_match_filename, matches_keyword

def test_exact_match_filename():
    """测试精确文件名匹配"""
    
    # 测试用例 1: 精确匹配（不考虑扩展名）
    assert exact_match_filename("报告.xlsx", "报告") == True
    assert exact_match_filename("报告.pdf", "报告") == True
    assert exact_match_filename("报告.docx", "报告") == True
    print("✓ 测试 1 通过：精确匹配（不同扩展名）")
    
    # 测试用例 2: 不匹配（包含额外词汇）
    assert exact_match_filename("年度报告.xlsx", "报告") == False
    assert exact_match_filename("2025年报告.pdf", "报告") == False
    print("✓ 测试 2 通过：不匹配（包含额外词汇）")
    
    # 测试用例 3: 大小写不敏感
    assert exact_match_filename("Report.xlsx", "report") == True
    assert exact_match_filename("REPORT.PDF", "report") == True
    print("✓ 测试 3 通过：大小写不敏感")
    
    # 测试用例 4: 部分匹配应该失败
    assert exact_match_filename("报告汇总.xlsx", "报告") == False
    assert exact_match_filename("项目报告.pdf", "报告") == False
    print("✓ 测试 4 通过：部分匹配失败")
    
    # 测试用例 5: 空关键词
    assert exact_match_filename("任意文件.txt", "") == True
    print("✓ 测试 5 通过：空关键词返回 True")
    
    # 测试用例 6: 中文测试
    assert exact_match_filename("财务预算.xlsx", "财务预算") == True
    assert exact_match_filename("财务预算分析.xlsx", "财务预算") == False
    print("✓ 测试 6 通过：中文精确匹配")
    
    print("\n✅ 所有精确匹配测试通过！")

def test_fuzzy_match():
    """测试模糊查找的高级功能仍然正常工作"""
    
    # 测试包含匹配
    assert matches_keyword("年度报告", "报告") == True
    assert matches_keyword("project_report", "report") == True
    print("✓ 测试 1 通过：包含匹配")
    
    # 测试逻辑与（必须包含）
    assert matches_keyword("项目报告2025", "+项目 +报告") == True
    assert matches_keyword("项目报告2025", "+项目 +总结") == False
    print("✓ 测试 2 通过：逻辑与")
    
    # 测试排除（不包含）
    assert matches_keyword("项目报告2025", "报告 -草稿") == True
    assert matches_keyword("项目报告草稿", "报告 -草稿") == False
    print("✓ 测试 3 通过：排除关键词")
    
    # 测试精确短语
    assert matches_keyword("季度财务报告", '"财务报告"') == True
    assert matches_keyword("财务 报告", '"财务报告"') == False
    print("✓ 测试 4 通过：精确短语")
    
    print("\n✅ 所有模糊查找测试通过！")

if __name__ == "__main__":
    print("=" * 50)
    print("FileGather Pro v2.3.5.1 - 精确查找功能测试")
    print("=" * 50)
    print()
    
    test_exact_match_filename()
    print()
    test_fuzzy_match()
    
    print()
    print("=" * 50)
    print("✅ 全部测试通过！精确查找功能正常工作")
    print("=" * 50)
