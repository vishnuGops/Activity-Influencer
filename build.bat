@echo off
echo Setting up environment variables...
set version=1.6
set exe_name=GitActivity_v%version%.exe

echo Generating executable file...
pyinstaller --onefile -n %exe_name% .\github_activity.py

if %errorlevel% equ 0 (
    echo Executable file "%exe_name%" successfully generated.
) else (
    echo Error: Failed to generate executable file. Please check the logs for more details.
)

echo Cleaning up intermediate files...
del .\%exe_name%.spec

echo Batch file execution completed.
