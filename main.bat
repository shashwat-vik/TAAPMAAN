@ECHO OFF
START /WAIT "UPDATE" CALL "Python35-32/scripts/cmd_j.bat" update.py scripts exit
START "SERVER" server.bat
