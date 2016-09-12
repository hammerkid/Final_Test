import commands
def port_find():
    status, output = commands.getstatusoutput("grep Port /etc/ssh/sshd_config")
    port = filter(str.isdigit,output)
    return port


ports = port_find()
print ports
