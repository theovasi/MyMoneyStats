import os
import getpass


def setup():
    pswd = getpass.getpass('Enter password:')
    with open('settings.cfg', 'w+') as settings_file:
        settings_file.write("SECRET_KEY={}\n".format(os.urandom(24)))
        settings_file.write("PASSWD='{}'".format(pswd))


if __name__ == '__main__':
    setup()

