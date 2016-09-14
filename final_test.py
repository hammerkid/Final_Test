import os, paramiko, re, json, yaml, pickle, mysql.connector


class Remote(object):
    ''''''
    def __init__(self):
        self.ip = '192.168.6.'
        self.ssh_user = 'pythonista'
        self.sql_user = 'root'
        self.ssh_password = 'letmein'
        self.port_ssh = 0
        self.client = None
        self.sql_passwd = ''


    def pinger(self):
        '''
        try ping remote server by iterate range of ip's
        and return correct ip addres
        '''
        try:
            for last_ip in range(80, 84):
                response = os.system('ping -c 1 {}{}'.format(self.ip, str(last_ip)))
                if response == 0:
                    self.ip += str(last_ip)
                    return self.ip
        except:
            return None

    def get_ssh_conector(self, port):
        host = self.ip
        user = self.ssh_user
        secret = self.ssh_password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=host, username=user, password=secret, port=port)
        except paramiko.ssh_exception.NoValidConnectionsError:
            return None
        else:
            return self.client

    def connected(self):
        for port in range(4110, 4201):
            client = self.get_ssh_conector(port)
            print ('tried connect to port {}'.format(str(port)))
            if client:
                self.port_ssh = str(port)
                print ('succeeded with port {}'.format(str(port)))
                return self.client, self.port_ssh

    def sql_passwd_find(self):
        search_passwd = re.compile('(?<=password=)(\w+)')
        self.client.exec_command('cd /home/pythonista')
        stdin, stdout, stderr = self.client.exec_command('grep -R password= *')
        data = stdout.read()
        self.sql_passwd = search_passwd.search(data).group()
        return self.sql_passwd

    def serialize_json(self):
        with open('nikitenko-server.json', 'w') as serv_output:
            json.dump((self.port_ssh, self.ip, self.ssh_user, self.ssh_password), serv_output)
            serv_output.close()
        return serv_output

    def serialize_mysql(self):
        with open('nikitenko-sql.yml', 'w') as sql_output:
            yaml.dump((self.sql_passwd, self.sql_user), sql_output)
            sql_output.close()
        return sql_output

    def bin_backup(self):
        with open('nikitenko-bin-backup', 'w') as bin_output:
            pickle.dump(('nikitenko-server.json', 'nikitenko-sql.yml'), bin_output)
            bin_output.close()
        return bin_output