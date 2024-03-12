echo Configuring environment
pip install pyinstaller >> setup_log.txt 2>&1
pip install tabulate >> setup_log.txt 2>&1
pip install psutil >> setup_log.txt 2>&1

touch /tmp/chopsticks_pipe.in
touch /tmp/chopsticks_pipe.out

if [ -f /usr/local/bin/cquit ]; then
    echo Chopsticks is already installed
    echo Try to terminate the running program
    cquit -f # avoid chopsticks is running
fi
echo Building chopsticks
pyinstaller -F src/guard.py >> setup_log.txt 2>&1
echo Setup service: credirect
pyinstaller -F src/credirect.py >> setup_log.txt 2>&1
echo Setup service: csubmit
pyinstaller -F src/csubmit.py >> setup_log.txt 2>&1
echo Setup service: ccancel
pyinstaller -F src/ccancel.py >> setup_log.txt 2>&1
echo Setup service: crestart
pyinstaller -F src/crestart.py >> setup_log.txt 2>&1
echo Setup service: cls
pyinstaller -F src/cls.py >> setup_log.txt 2>&1
echo Setup service: cclean
pyinstaller -F src/cclean.py >> setup_log.txt 2>&1
echo Setup service: cquit
pyinstaller -F src/cquit.py >> setup_log.txt 2>&1
mv dist/guard dist/chopsticks

echo Install chopsticks
sudo cp dist/* /usr/local/bin/
echo Finish setup, check more information in setup_log.txt
