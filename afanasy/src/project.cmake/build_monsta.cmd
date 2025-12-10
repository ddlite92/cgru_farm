@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

set PATH=C:\Qt\5.15.2\msvc2019_64\bin;C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin;%PATH%
set AF_GUI=YES
set AF_OSTYPE=windows
set AF_POSTGRESQL=NO
set CGRU_VERSION=3.14
set CGRU_REVISION=MonstaFarm

echo Cleaning previous build...
if exist CMakeCache.txt del CMakeCache.txt
if exist CMakeFiles rmdir /s /q CMakeFiles

echo Configuring with CMake...
cmake -G "Visual Studio 17 2022" -A x64 .

echo Building afwatch...
cmake --build . --target afwatch --config Release

echo Done!
pause
