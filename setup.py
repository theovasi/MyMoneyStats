import os
import getpass
from passlib.hash import pbkdf2_sha256


def setup():
    pswd = getpass.getpass('Enter password:')
    pswd_hash = pbkdf2_sha256.hash(pswd)
    with open('settings.cfg', 'w+') as settings_file:
        settings_file.write("SECRET_KEY={}\n".format(os.urandom(24)))
        settings_file.write("PASSWD='{}'".format(pswd_hash))


if __name__ == '__main__':
    setup()

