@echo off 

set /p mode="Enter 0 for auto ethernet configuration, 1 - for manual: "

if %mode% == 0 (
    netsh interface ip set address name="Ethernet" source=dhcp
    netsh interface ip set dns name="Ethernet" source=dhcp
    goto:correct_execution
)

if %mode% == 1 (
    netsh interface ip set address name="Ethernet" source=static addr=192.168.1.10 mask=255.255.255.0 gateway=192.168.1.1
    netsh interface ip set dns name="Ethernet" source=static addr=8.8.8.8 >nul
    goto:correct_execution
)

echo Input mode is incorrect

:correct_execution
pause