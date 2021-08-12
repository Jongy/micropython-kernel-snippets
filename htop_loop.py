# spin an alpine container running "sh"

sh = pgrep("sh")
sh.pid

# run 2nd shell

ps()

# enter its PID:
sh2 = pgrep_pid(...)

# these should match
sh2.real_parent.pid
sh.pid

# htop in tree mode

p = sh.real_parent
sh.real_parent = sh2

# ps -o comm,pid,ppid
# loop!

# try htop in tree mode...

sh.real_parent = p

# try htop again
