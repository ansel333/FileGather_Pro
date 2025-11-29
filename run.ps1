#!/usr/bin/env pwsh
<#
.SYNOPSIS
快速启动 FileGather Pro 应用

.DESCRIPTION
激活 Python 虚拟环境并启动 FileGather Pro 2.3.5.1

.EXAMPLE
.\run.ps1

#>

# 获取脚本所在目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      FileGather Pro v2.3.5.1 - 快速启动脚本               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 检查虚拟环境是否存在
$venvPath = ".\.venv311\Scripts\Activate.ps1"
if (-not (Test-Path $venvPath)) {
    Write-Host "❌ 错误：未找到虚拟环境 .venv311" -ForegroundColor Red
    Write-Host "请先运行以下命令创建虚拟环境：" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv311" -ForegroundColor Yellow
    Write-Host "  .venv311\Scripts\pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# 检查主文件是否存在
$mainFile = ".\FileGather_Pro.py"
if (-not (Test-Path $mainFile)) {
    Write-Host "❌ 错误：未找到主文件 $mainFile" -ForegroundColor Red
    exit 1
}

Write-Host "✓ 虚拟环境检查通过" -ForegroundColor Green
Write-Host "✓ 主文件检查通过" -ForegroundColor Green
Write-Host ""

# 激活虚拟环境并启动应用
Write-Host "🚀 启动应用中..." -ForegroundColor Yellow
Write-Host ""

& $venvPath
python $mainFile

# 应用关闭时显示信息
Write-Host ""
Write-Host "👋 应用已关闭" -ForegroundColor Cyan
