pip install pyinstaller
pip install psutil 

touch /tmp/chopsticks_pipe.in
touch /tmp/chopsticks_pipe.out

cquit # avoid chopsticks is running
pyinstaller -F src/guard.py 
pyinstaller -F src/credirect.py 
pyinstaller -F src/csubmit.py 
pyinstaller -F src/ccancel.py 
pyinstaller -F src/cls.py 
pyinstaller -F src/cclean.py 
pyinstaller -F src/cquit.py 
mv dist/guard dist/chopsticks
sudo cp dist/* /usr/local/bin/