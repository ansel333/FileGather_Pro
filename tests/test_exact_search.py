#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for exact filename matching functionality
"""

import os
import sys

# Set Qt platform before any Qt imports
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set output encoding
if sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from components.search_logic import exact_match_filename, matches_keyword

def test_exact_match_filename():
    """Test exact filename matching"""
    
    # Test case 1: Exact match (ignoring extension)
    assert exact_match_filename("报告.xlsx", "报告") == True
    assert exact_match_filename("报告.pdf", "报告") == True
    assert exact_match_filename("报告.docx", "报告") == True
    print("✓ Test 1 passed: Exact match (different extensions)")
    
    # Test case 2: Non-match (contains extra words)
    assert exact_match_filename("年度报告.xlsx", "报告") == False
    assert exact_match_filename("2025年报告.pdf", "报告") == False
    print("✓ Test 2 passed: Non-match (contains extra words)")
    
    # Test case 3: Case insensitive
    assert exact_match_filename("Report.xlsx", "report") == True
    assert exact_match_filename("REPORT.PDF", "report") == True
    print("✓ Test 3 passed: Case insensitive")
    
    # Test case 4: Partial matches should fail
    assert exact_match_filename("报告汇总.xlsx", "报告") == False
    assert exact_match_filename("项目报告.pdf", "报告") == False
    print("✓ Test 4 passed: Partial matches fail")
    
    # Test case 5: Empty keyword
    assert exact_match_filename("任意文件.txt", "") == True
    print("✓ Test 5 passed: Empty keyword returns True")
    
    # Test case 6: Chinese tests
    assert exact_match_filename("财务预算.xlsx", "财务预算") == True
    assert exact_match_filename("财务预算分析.xlsx", "财务预算") == False
    print("✓ Test 6 passed: Chinese exact match")
    
    print("\n✅ All exact match tests passed!")

def test_fuzzy_match():
    """Test advanced functionality of fuzzy matching still works"""
    
    # Test contains matching
    assert matches_keyword("年度报告", "报告") == True
    assert matches_keyword("project_report", "report") == True
    print("✓ Test 1 passed: Contains matching")
    
    # Test logical AND (must contain)
    assert matches_keyword("项目报告2025", "+项目 +报告") == True
    assert matches_keyword("项目报告2025", "+项目 +总结") == False
    print("✓ Test 2 passed: Logical AND")
    
    # Test exclusion (not contains)
    assert matches_keyword("项目报告2025", "报告 -草稿") == True
    assert matches_keyword("项目报告草稿", "报告 -草稿") == False
    print("✓ Test 3 passed: Exclude keywords")
    
    # Test exact phrase
    assert matches_keyword("季度财务报告", '"财务报告"') == True
    assert matches_keyword("财务 报告", '"财务报告"') == False
    print("✓ Test 4 passed: Exact phrase")
    
    print("\n✅ All fuzzy match tests passed!")

if __name__ == "__main__":
    print("=" * 50)
    print("FileGather Pro v2.4.0 - Exact Search Functionality Test")
    print("=" * 50)
    print()
    
    test_exact_match_filename()
    print()
    test_fuzzy_match()
    
    print()
    print("=" * 50)
    print("✅ All tests passed! Exact search functionality working")
    print("=" * 50)
