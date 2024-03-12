if [ -f /usr/local/bin/cquit ]; then
    echo Chopsticks is already installed
    echo Try to terminate the running program
    cquit -f # avoid chopsticks is running
fi

echo Uninstall chopsticks
sudo rm /usr/local/bin/chopsticks
sudo rm /usr/local/bin/csubmit
sudo rm /usr/local/bin/ccancel
sudo rm /usr/local/bin/cls
sudo rm /usr/local/bin/crestart
sudo rm /usr/local/bin/cclean
sudo rm /usr/local/bin/cquit
echo Finish uninstall