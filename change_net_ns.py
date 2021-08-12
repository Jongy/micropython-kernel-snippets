# spin an alpine container running "sh"

sh = pgrep("sh")
sh.pid

sh.nsproxy.net_ns

# run ifconfig

init_net

x = sh.nsproxy.net_ns

# run ifconfig again

sh.nsproxy.net_ns = int(init_net)

sh.nsproxy.net_ns = x
