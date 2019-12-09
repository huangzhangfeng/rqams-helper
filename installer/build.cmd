if "%1"=="release" (
    set /P version=<rqams_helper/VERSION.txt
) ELSE (
    set version=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
)

set name=RQAmsHelperInstaller_%version%

cd installer
pyinstaller rqams-helper.py -w -i ../rqams_helper/windows/resources/icon.ico
iscc installer.iss /F%name%
cd ..
