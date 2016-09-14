import os, paramiko, re, json, yaml, pickle, mysql.connector
from mysql.connector import Error


class Remote(object):
    ''''''
    def __init__(self):
        self.ip = '192.168.6.'
        self.ssh_user = 'pythonista'
        self.sql_user = 'root'
        self.ssh_password = 'letmein'
        self.ssh_port = 0
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
        '''Trying setup connetion,
        need for conneted func,
        that try get valid port'''
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
            print ('Connected')
            return self.client

    def connected(self):
        '''By iterate through range, try get valid port
        and when its found return ssh client and port'''
        for port in range(4110, 4201):
            client = self.get_ssh_conector(port)
            print ('tried connect to port {}'.format(str(port)))
            if client:
                self.ssh_port = str(port)
                print ('succeeded with port {}'.format(str(port)))
                return self.client, self.ssh_port

    def sql_passwd_find(self):
        '''find passwd to mysql by parsing files via grep
        then read it to variable and get passwd with regexp and
        return it'''
        search_passwd = re.compile('(?<=password=)(\w+)')
        self.client.exec_command('cd /home/pythonista')
        stdin, stdout, stderr = self.client.exec_command('grep -R password= *')
        data = stdout.read()
        self.sql_passwd = search_passwd.search(data).group()
        return self.sql_passwd

    def serialize_json(self):
        with open('nikitenko-server.json', 'w') as serv_output:
            json.dump((self.ssh_port, self.ip, self.ssh_user, self.ssh_password), serv_output)
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

    def db_maker(self):
        '''http://www.internet-technologies.ru/articles/article_2190.html
        create database via client ssh then use mysql connector for creating tables'''
        self.client.exec_command('mysql -u root -p {}'.format(self.sql_passwd))
        self.client.exec_command('CREATE DATABASE Nikitenko')
        try:
            conn = mysql.connector.connect(host='{}@{}:{}'.format(self.ssh_user, self.ssh_password, self.ssh_port),
                                           database='Nikitenko',
                                           user=self.sql_user,
                                           password=self.sql_passwd)
            if conn.is_connected():
                print('Connected to MySQL database')

        except Error as e:
            print(e)

        finally:
            conn.close()
