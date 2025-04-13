@echo off
echo helloWorld > c:/Temp/sometempfile.txt
set "timestamp=%date:/=-% %time::=-%"
set "timestamp=%timestamp: =_%"
echo Starting hourly_auto.bat > c:/Temp/hourly_logs/log_hourly_auto_%timestamp%.txt
cd c:/z/python/koop/gentraffic/inputfiles && DEL prev.csv
cd c:/z/python/koop/gentraffic/inputfiles && REN traffic.csv prev.csv
cd c:/z/python/koop/gentraffic/inputfiles && DEL traffic.csv 
cd c:/z/python/koop/gentraffic && C:/Users/MM/AppData/Local/Programs/Python/Python310/python check_email_and_run_auto_gentraffic.py >> c:/Temp/hourly_logs/log_hourly_auto_%timestamp%.txt 2>&1
echo Finished hourly_auto.bat >> c:/temp/hourly_logs/log_hourly_auto_%timestamp%.txt
