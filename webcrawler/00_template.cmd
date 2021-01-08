rem 
rem 00_template.cmd
rem

set PYTHONIOENCODING=UTF-8

if "%00_template_home%" == "" goto do_init

goto skip_init

:do_init
set 00_template_home=CONFIGURE HERE 
set PYTHONPATH=%00_template_home%;%00_template_home%\src
set PYTHON_HOME=%00_template_home%
set PATH=%PYTHON_HOME%\Scripts\;%PATH%
set PYTHON_EXE=%PYTHON_HOME%\Scripts\python.exe

:skip_init

"%PYTHON_EXE%" -u %00_template_home%\main.py ^
--config="config.yaml" ^
--logging="logging.json" ^
%1 %2 %3 %4 %5



