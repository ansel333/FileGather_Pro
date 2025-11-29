"""
PyInstaller build script for FileGather_Pro
Generates a standalone .exe file
"""

import os
import sys
from pathlib import Path

# Get the absolute path of the project directory
project_dir = Path(__file__).parent.absolute()
main_file = project_dir / "FileGather_Pro.py"
icon_file = project_dir / "app.ico"

# PyInstaller command
pyinstaller_cmd = [
    "pyinstaller",
    "--name=FileGather_Pro",
    "--onefile",  # Single executable file
    "--windowed",  # No console window
    "--add-data=components:components",  # Include components package
    f"--icon={icon_file}",  # Application icon
    "--distpath=dist",  # Output directory
    "--buildpath=build",  # Build directory
    "--specpath=.",  # Spec file location
    "--clean",  # Clean before building
    str(main_file)
]

# Print the command
print(f"Building FileGather_Pro.exe...")
print(f"Command: {' '.join(pyinstaller_cmd)}")

# Run PyInstaller
os.system(" ".join(pyinstaller_cmd))

print("\nBuild complete!")
print(f"Output: {project_dir / 'dist' / 'FileGather_Pro.exe')")


