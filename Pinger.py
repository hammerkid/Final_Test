import os
def pinger():
    x = 1
    good_ip = []
    try:
        for _ in range(0, 10):
            response = os.system('ping -c 1 192.168.6.{}'.format(x))
            x += 1
            if response == 0:
                good_ip.append(x)
    except:
        pass


ping = pinger()