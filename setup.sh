sh uninstall.sh

echo Configuring environment
pip install pyinstaller >> setup_log.txt 2>&1
pip install tabulate >> setup_log.txt 2>&1
pip install psutil >> setup_log.txt 2>&1

echo Building chopsticks
pyinstaller -F src/guard.py >> setup_log.txt 2>&1
pyinstaller -F src/cs.py >> setup_log.txt 2>&1
mv dist/guard dist/chopsticks

echo Install chopsticks
sudo cp dist/* /usr/local/bin/
echo Finish setup, check more information in setup_log.txt