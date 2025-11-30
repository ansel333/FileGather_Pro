#!/usr/bin/env python3
"""
构建验证脚本 - 检查 GitHub Actions 工作流文件的有效性
Workflow validation script - Check GitHub Actions workflow files validity
"""

import os
import sys
import yaml
from pathlib import Path

def validate_workflow(workflow_path):
    """验证单个工作流文件"""
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow = yaml.safe_load(f)
        
        # 检查基本结构
        required_keys = {'name', 'on', 'jobs'}
        missing_keys = required_keys - set(workflow.keys())
        
        if missing_keys:
            print(f"❌ {workflow_path.name}: 缺少必需键: {missing_keys}")
            return False
        
        # 检查 jobs
        jobs = workflow.get('jobs', {})
        if not jobs:
            print(f"❌ {workflow_path.name}: 没有定义任何 jobs")
            return False
        
        print(f"✅ {workflow_path.name}")
        print(f"   - Name: {workflow.get('name')}")
        print(f"   - Jobs: {', '.join(jobs.keys())}")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ {workflow_path.name}: YAML 解析错误")
        print(f"   {str(e)}")
        return False
    except Exception as e:
        print(f"❌ {workflow_path.name}: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("FileGather Pro - GitHub Actions 工作流验证")
    print("=" * 60)
    print()
    
    workflows_dir = Path(__file__).parent / "workflows"
    
    if not workflows_dir.exists():
        print(f"❌ 工作流目录不存在: {workflows_dir}")
        return 1
    
    workflow_files = sorted(workflows_dir.glob("*.yml"))
    
    if not workflow_files:
        print(f"❌ 未找到工作流文件")
        return 1
    
    print(f"找到 {len(workflow_files)} 个工作流文件:")
    print()
    
    all_valid = True
    for workflow_path in workflow_files:
        if not validate_workflow(workflow_path):
            all_valid = False
        print()
    
    print("=" * 60)
    if all_valid:
        print("✅ 所有工作流文件验证成功!")
        print()
        print("工作流概览:")
        print("  1. build-all-platforms.yml     - 所有平台（推荐）")
        print("  2. build-windows-11-intel.yml  - Windows 专用")
        print("  3. build-macos.yml             - macOS (Intel & Apple Silicon)")
        print("  4. build-linux-deb.yml         - Linux .deb 包")
        return 0
    else:
        print("❌ 部分工作流文件验证失败")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)
