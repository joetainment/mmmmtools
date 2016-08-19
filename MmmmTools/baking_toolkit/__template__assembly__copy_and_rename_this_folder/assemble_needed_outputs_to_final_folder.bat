@echo off
echo WARNING - This is dangerous if you've edited files in the unity project!!!
echo   they will be overwritten if so
echo   since we are copying to the unity project and overwrite is auto-on
echo   close this window (use the mouse) without pushing
echo   any keyboard keys to cancel now!
pause
pause
pause

REM   **** Replace the paths below with your own relevant paths! ****
REM        eg.    ..\..\..\SomeExampleFolder\
REM        eg.    C:\users\public\SomeExampleFolder\
REM        See additional examples below for exact copy commands
REM        the  "/y" is include to make it not ask about overwriting
REM        however, you may wish to remove the "/y" for your own use
cd %~dp0

REM copy /y *__diff__tex.png :REPLACE-THIS-FOLDER-LOCATION:\
REM copy /y *__emis__tex.png :REPLACE-THIS-FOLDER-LOCATION:\
REM copy /y *__spec__tex.tga :REPLACE-THIS-FOLDER-LOCATION:\
REM copy /y *__norm__tex.png :REPLACE-THIS-FOLDER-LOCATION:\
REM copy /y *__mesh.fbx :REPLACE-THIS-FOLDER-LOCATION:\



pause
