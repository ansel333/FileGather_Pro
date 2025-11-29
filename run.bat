@echo off
REM FileGather Pro v2.3.5.1 - 快速启动脚本（批处理版本）
REM 用于 Windows 环境下直接运行

title FileGather Pro v2.3.5.1

echo.
echo ============================================================
echo      FileGather Pro v2.3.5.1 - 快速启动脚本
echo ============================================================
echo.

REM 检查虚拟环境
if not exist ".venv311\Scripts\activate.bat" (
    echo.
    echo 错误：未找到虚拟环境 .venv311
    echo 请先运行以下命令创建虚拟环境：
    echo   python -m venv .venv311
    echo   .venv311\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM 检查主文件
if not exist "FileGather_Pro.py" (
    echo.
    echo 错误：未找到主文件 FileGather_Pro.py
    echo.
    pause
    exit /b 1
)

echo 虚拟环境检查通过 ✓
echo 主文件检查通过 ✓
echo.
echo 启动应用中...
echo.

REM 激活虚拟环境并运行应用
call .venv311\Scripts\activate.bat
python FileGather_Pro.py

echo.
echo 应用已关闭
echo.
pause
