import os, re

def passwd_find():
    search_passwd = re.compile('(?<=password=)(\w+)')
    path = '/home/pythonista'
    for file in os.listdir(path):
        with open(file) as f:
            for line in f:
                passwd = search_passwd.search(line).group()
    return passwd
