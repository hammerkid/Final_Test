import os,paramiko,re
# def pinger():
#     x=80
#     good_ip = []
#     ip = '192.168.6.'
#     try:
#         for _ in range(0, 4):
#             response = os.system('ping -c 1 {}{}'.format(ping,x))
#             x += 1
#             if response == 0:
#                 good_ip.append(x-1)
#                 ip +=x-1
#         return good_ip, ip
#     except:
#         pass
# ping = pinger()


def get_ssh_conecter(port):
    host = '192.168.6.82'
    user = 'pythonista'
    secret = 'letmein'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, username=user, password=secret, port=port)
    except paramiko.ssh_exception.NoValidConnectionsError:
        return None
    else:
        return client

def port_finder():
    for port in range(4110,4201):
        c = get_ssh_conecter(port)
        print ('tried connect to port {}'.format(port))
        if c:
            print ('succeeded with port {}'.format(port))
            return c

def passwd_find():
    search_passwd = re.compile('(?<=password=)(\w+)')
    stdin, stdout, stderr = client.exec_command('cd /home/pythonista')
    path = '/home/pythonista'
    passwd = search_passwd.search('password=exam').group()
    return passwd




passwd_find()
