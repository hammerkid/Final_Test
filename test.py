import re
search_passwd = re.compile('(?<=password=)(\w+)')
passwd = search_passwd.search('asdfasdf password=weqeqfds2 fdsfa 324 fdsfewf43fe').group()
print passwd