# Chopsticks🥢

> A **sequential** task manager for Linux and MacOS

### Who need this

- If you use a single computing node, and often run complex computing jobs, limited by hardware bottlenecks (RAM size, GPU memory size, number of CPU cores, etc.)
- When you are ready to leave, and the tasks you have submitted has not yet finished running, but you still wanna append some new tasks so that it has done more work when you come back.

### Who don't need this

- If you have a large-scale computing cluster that can sufficiently parallelize the submitted tasks, please use SLURM.
- If your computing tasks do not take up very much hardware resources, please submit them manually in the terminal directly, don't worry about them being interrupted.

![Chopsticks.gif](https://s2.loli.net/2023/04/07/Y1O3G2udeV597Jg.gif)

## Get Started

### Requirements

- Python >= 3.6

### Install

```bash
git clone https://github.com/InkosiZhong/Chopsticks.git
cd Chopsticks
sh setup.sh
```

> `setup.sh` needs root permissions to install at /usr/local/bin
>
> **Or** you can manually setup  `dist` into the path

### Usage

Chopsticks supports 6 commands: redirect, submit, cancel, ls, clean, quit, you can use them starting with  `c` , the first letter of the Chopsticks

#### creidirect

```bash
credirect out # redirect the output into a file
credirect /dev/pts/5 # redirect to a terminal
credirect # or redirect to current terminal
```

#### csubmit

```bash
csubmit command arg1 arg2 ...
# Example
# if you have a add.py that input 2 args, such as
python test.py 0 1
# now you can submit them only by adding csubmit
csubmit python test.py 0 1
# Chopsticks will give you an unique id for this task
> [submit] id=0
```

#### ccancel

```bash
ccancel id # cancel a specified task
ccancel # cancel all tasks that are waiting
# Example
csubmit python test.py 0 1
> [submit] id=0
csubmit python test.py 0 1
> [submit] id=1
ccancal 1
> [cancel] id=1
```

#### cls

> Note: `argparser` enabled

```bash
usage: cls [-h] [-l] [-p] [-n LATEST_N] [--done] [--not-done]
optional arguments:
  -h, --help            show this help message and exit
  -l, --long            show long info
  -p, --pid             show PID
  -n LATEST_N, --latest-n LATEST_N
                        show the latest n records
  --done                show the records that are already finished|crashed|cancelled
  --not-done            show the records that are still running|waiting
# Example
cls
>
  id  state      submit    command
----  ---------  --------  ------------------
   0  finished   22:35:02  python test.py 0 1
   1  cancelled  22:35:03  python test.py 0 1

cls -n 1 # the latest one
>
  id  state      submit    command
----  ---------  --------  ------------------
   1  cancelled  22:35:03  python test.py 0 1
   
cls -n 1 -l --done # the latest one that is done
>
  id  state      submit    start     end       duration        command
----  ---------  --------  --------  --------  --------------- ------------------
   1  cancelled  22:35:03  22:35:03  22:35:03  0 days 00:00:00 python test.py 0 1
```

#### cclean

```bash
cclean
# Example
cclean
> [clean] 2 tasks
cls
>
  id  state      submit    command
----  ---------  --------  ------------------
```

#### cquit

> Note: `argparser` enabled

```bash
usage: cquit [-h] [-f]
optional arguments:
  -h, --help   show this help message and exit
  -f, --force  quit anyway, ignoring the running|waiting tasks
```

## Known Issues and Solution

#### 1. Output of the running task can not be redirect

Since I use the most intuitive method to implement the redirection part, once the task starts executing, it cannot be modified. In addition, all outputs are in the same file or terminal now. In the future Chopsticks may be support for redirecting to a different file for each task.

#### 2. Doesn't support interactive tasks

Chopsticks exists to handle large-scale computing tasks, interactive tasks are not considered, please submit manually in the terminal.

#### 3. Runtime environment

Chopsticks temporarily does not support different tasks to run in different environments, it mainly depends on the running environment of the guard process. If you want to modify the running environment (such as conda environment), please execute following commands

```bash
(base) cquit
(base) conda activate env
(env) credirect # or any other commands
> [trigger] start a guard process
> [guard] guard process ready
> [redirect] set as /tmp/out.txt
> [trigger] the above outputs are antique
```