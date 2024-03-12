echo Uninstall chopsticks
if [ -f /usr/local/bin/cquit ]; then
    echo found Chopsticks v1.x
    echo Try to terminate the running program
    cquit -f # avoid chopsticks is running
    sudo rm /usr/local/bin/credirect
    sudo rm /usr/local/bin/csubmit
    sudo rm /usr/local/bin/ccancel
    sudo rm /usr/local/bin/cls
    sudo rm /usr/local/bin/crestart
    sudo rm /usr/local/bin/cclean
    sudo rm /usr/local/bin/cquit
    if [ -f /tmp/chopsticks_pipe.in ]; then
        sudo rm /tmp/chopsticks_pipe.in
    fi
    if [ -f /tmp/chopsticks_pipe.out ]; then
        sudo rm /tmp/chopsticks_pipe.out
    fi
fi
if [ -f /usr/local/bin/cs ]; then
    echo found Chopsticks v2.x
    echo Try to terminate the running program
    cs quit -f # avoid chopsticks is running
    sudo rm /usr/local/bin/cs
    if [ -d /tmp/chopsticks ]; then
        sudo rm -r /tmp/chopsticks
    fi
fi
if [ -f /usr/local/bin/chopsticks ]; then
    sudo rm /usr/local/bin/chopsticks
else
    echo Chopsticks not found
fi
echo Finish uninstall