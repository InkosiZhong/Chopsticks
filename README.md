# Chopsticks🥢

> A **sequential** task manager for Linux and MacOS

### Who need this

- If you use a single computing node, and often run complex computing jobs, limited by hardware bottlenecks (RAM size, GPU memory size, number of CPU cores, etc.)
- When you are ready to leave, and the tasks you have submitted has not yet finished running, but you still wanna append some new tasks so that it has done more work when you come back.

### Who don't need this

- If you have a large-scale computing cluster that can sufficiently parallelize the submitted tasks, please use SLURM.
- If your computing tasks do not take up very much hardware resources, please submit them manually in the terminal directly, don't worry about them being interrupted.

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

> Note: Chopsticks is only a very basic implementation. Since the bottom layer is implemented by the futhure package, **it does not support the cancellation of the running task.**
>
> If you want to cancel the running task, you have to use `kill pid`.

```bash
ccancel id 	# cancel a specified task
ccancel 		# cancel all tasks that are waiting
# Example
csubmit python test.py 0 1
> [submit] id=0
csubmit python test.py 0 1
> [submit] id=1
ccancal 1
> [cancel] id=1
```

#### cls

```bash
cls n			# show the last-n tasks
cls 			# show all tasks
# Example
cls
>
  id  state      submit    start     end       command
----  ---------  --------  --------  --------  ------------------
   0  finished   22:35:02  22:35:02  22:35:02  python test.py 0 1
   1  cancelled  22:35:03  22:35:03  22:35:03  python test.py 0 1
```

#### cclean

```bash
cclean
# Example
cclean
> [clean] 2 tasks
cls
>
  id  state      submit    start     end       command
----  ---------  --------  --------  --------  ------------------
```

#### cquit

```bash
cquit				# quit if all tasks are finished
cquit force # cancal the waiting tasks and ignore the running task
```

