from cryptography.fernet import Fernet

secret_key = 'tNXSr3w1v29_cBJhhN16BXNh_nVu7pmtD61KYnfmwK4='


def lock_file(path, key):
    fernet = Fernet(key)

    with open(path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(path, 'wb') as en_file:
        en_file.write(encrypted)


def unlock_file(path, key):
    fernet = Fernet(key)

    with open(path, 'rb') as file:
        enc = file.read()

    decrypted = fernet.decrypt(enc)

    with open(path, 'wb') as file:
        file.write(decrypted)


def decrypt_file(path, key):
    fernet = Fernet(key)

    with open(path, 'rb') as file:
        enc = file.read()

    return fernet.decrypt(enc).decode()


if __name__ == '__main__':
    # lock_file('common/statistics #2.dat', secret_key)
    print(decrypt_file('common/statistics #2.dat', secret_key).replace('\r', '').split('\n'))
    # unlock_file('testthing.txt', secret_key)
