:loop
@echo off
echo Starting bot...
echo bot by EagleEye
python botfeed.py
echo Bot stopped. Restarting in 10 seconds...
timeout /t 10
goto loop
