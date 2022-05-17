import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "packages": ["os", "sys", "thorpy", "pygame", "numpy", "tkinter"], 
    "excludes": [""],
    "includes": ["thorpy", "pygame", "numpy", "tkinter"],
    "include_files": ["images", "sound"],
    "include_msvcr": True
}

bdist_msi_options = {
    "summary_data": {
        "author": "Sharang Sawleshwarkar",
        "comments": "Testing out executables",
        "keywords": "SnakeGame",
    },
}
# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI"
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="SnakeGame",
    version="1.1",
    description="Snake Game",
    options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
    executables=[Executable("main.py", base=base)],
)