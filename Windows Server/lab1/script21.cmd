@echo off

set /p "STR=Please enter 4 symbol string: "

echo %STR% | findstr /r "\<[A-Za-z0-9_][A-Za-z0-9_][A-Za-z0-9_][A-Za-z0-9_]\>" >nul 2>&1
echo.

if errorlevel 1 (
    echo Input string is incorrect
    goto:incorrect_input
) 

set username=UPart2%STR%
set groupname=GPart2%STR%

net user %username% >nul 2>&1

if %errorlevel% EQU 0 (
    echo User with this name already exists
    goto:incorrect_input
)

net localgroup %groupname% >nul 2>&1

if %errorlevel% EQU 0 (
    echo Group with this name already exists
    goto:incorrect_input
)

net user %username% /add >nul 2>&1
echo Successfully created new user %username%

net localgroup %groupname% /add >nul 2>&1
echo Successfully created new group %groupname%

net localgroup %groupname% %username% /add >nul 2>&1
echo Successfully added user %username% to group %groupname%

net user %username% /active:yes >nul 2>&1
echo Successfully activated user %username%

:incorrect_input
pause