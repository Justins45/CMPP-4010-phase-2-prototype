@echo off
@REM This Script runs the program (server + client) python files

@REM set local directory as working directory
cd /d %~dp0 

@REM --- Check if Docker is running ---
echo Checking Docker status...
docker info >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo Docker does NOT appear to be running.
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
) ELSE (
    echo Docker is running. Proceeding with setup...
)


@REM Build docker containers and run in background
@REM && runs second command ONLY if the first command is successful
docker-compose build --no-cache && docker-compose up -d 

@REM start is to open the command in a new terminal 

start "SERVER_LOGS" cmd /k docker-compose logs -f server
start "CLIENT_LOGS" cmd /k docker-compose exec client python3 -u main.py

@REM Pause terminal and allow user to shut it all down when they are done.
echo.
echo Press any key to shut everything down...
pause >nul

echo Stopping containers...
docker-compose down
exit
