@echo off
echo Setting up environment variables...
set version=1.9
set exe_name=GitActivity_v%version%.exe

echo Generating executable file...
pyinstaller --onefile -n "%exe_name%" .\github_activity.py

if %errorlevel% equ 0 (
    echo Executable file "%exe_name%" successfully generated.

@REM echo Executable name: "%exe_name%"
@REM     echo Creating shortcut...
@REM     echo Checking contents of the 'dist' directory...
@REM     set shortcut_target=dist\%exe_name%
@REM     set startup_folder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
@REM     set shortcut_name=GitActivity.lnk
@REM     set shortcut_file=%startup_folder%\%shortcut_name%
    
@REM     echo Shortcut target: %shortcut_target%
@REM     echo Shortcut file: "%shortcut_file%"
    
@REM     echo Creating new shortcut...
@REM     if exist dist\%exe_name% (
@REM         copy "dist\%exe_name%" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
@REM         echo Shortcut created successfully.
@REM     ) else (
@REM         echo Error: Executable file not found. Please check the logs for more details.
@REM     )
) else (
    echo Error: Failed to generate executable file. Please check the logs for more details.
)

echo Cleaning up intermediate files...
del ".\%exe_name%.spec"

echo Batch file execution completed.
