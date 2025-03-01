@echo off

rem -----------------------------------------------------------------------
rem Check command line parameters
rem -----------------------------------------------------------------------
if "%1"==""   goto usage
if "%1"=="?"  goto usage
if "%1"=="-?" goto usage
if "%1"=="-h" goto usage
if "%1"=="--help" goto usage
goto %1
goto _eof

:usage
echo -----------------------------------------------------------------
echo Project makefile
echo -----------------------------------------------------------------
echo make pip		    Upgrade requirements with pip
echo make pylint        Run pylint on the whole source folder
echo make flake8        Run flake 8 on the whole source folder
echo make vulture       Find dead code
echo.
echo make pip           Install all (updated) requirements.
rem echo make ui2py         Convert QT5 UIO design file to py design file
echo make clean         Clean up temporary file
echo.
echo make sphinx        Generate sphinx user documentation
rem echo make apidoc        Generate sphinx api documentation
echo make doxygen       Make doxygen documentation
echo.
echo make installer      make full installation (py2exe and nsis installer)
echo make doxygen        make doxygen documentation
echo.
goto _eof


rem --- Run pylint
:pylint
pylint src --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --reports n --disable E0611,C0301 --extension-pkg-whitelist=win32api 
goto _eof

rem --- Run flake8 
:flake8
flake8.exe --max-complexity 10 --max-line-length 120 src
goto _eof

rem --- Run vulture to detect unused functions and/or variables
:vulture
pushd src
vulture.exe . --exclude=venv,lib,tracetool.py,dict4ini.py,cmd2.py
popd
goto _eof

rem --- Update Python libraries (using requirements.txt)
:pip
python.exe -m pip install --upgrade pip
pip install -r requirements_dev.txt --upgrade
goto _eof

rem --- convert QT designer UI file to .py file
REM :ui2py
REM pushd src
REM rem pyside2-uic.exe esp32shell_qt_design.ui -o esp32shell_qt_design.py
REM C:\Users\HenkA\AppData\Local\Programs\Python\Python38\Scripts\pyuic5.exe esp32shell_qt_design.ui -o esp32shell_qt_design.py
REM popd
REM goto _eof

rem --- Generate DOXYGEN documentation
:doxygen
pushd docs
call doxygen 
popd
start ./docs/doxygen/html/index.html
goto _eof
	
rem :show_doxygen
rem rem "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" .\doc\doxygen\html\index.html
rem start ./docs/doxygen/html/index.html
rem goto _eof

:sphinx
pushd docs & call make html & popd
rem "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" .\doc\_build\html\index.html
start ./docs/_build/html/index.html
goto _eof
    
    
:pyinstaller
REM REM --- Create the CLI executable with all supporting python files
REM pyinstaller src\esp32cli.py
REM REM --- Create the standalone CLI executable 
REM pyinstaller --onefile src\esp32cli.py
REM REM --- Create the GUI executable with all supporting python files
REM pyinstaller src\esp32gui.py
REM REM --- Create the standalone GUI executable 
REM pyinstaller --onefile src\esp32gui.py   
REM goto _eof
    
:mypy
pushd src
mypy .
popd 
goto _eof

:clean
del /S /Q *.bak
pushd src & rmdir /S /Q __pycache__ & popd
pushd src & rmdir /S /Q .mypy_cache & popd
rmdir /S /Q .mypy_cache
pushd tests & rmdir /S /Q __pycache__ & popd
pushd tests & rmdir /S /Q .pytest_cache & popd
pushd docs\doxygen & rmdir /S /Q html & popd
pushd docs & rmdir /S /Q _build & popd
pushd doc & make clean & popd
goto _eof
	

:_eof
