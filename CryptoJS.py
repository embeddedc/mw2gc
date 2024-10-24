## https://gist.github.com/sh4dowb/efab23eda2fc7c0172c9829cf34dc96c

import base64
from Crypto.Hash import MD5
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import secrets

def decrypt(ciphertext, password):
    encryptedData = base64.b64decode(ciphertext)

    salt = encryptedData[8:16]
    ciphertext = encryptedData[16:]

    derived = b""
    while len(derived) < 48:  # "key size" + "iv size" (8 + 4 magical units = 12 * 4 = 48)
        hasher = MD5.new()
        hasher.update(derived[-16:] + password.encode('utf-8') + salt)
        derived += hasher.digest()

    key = derived[0:32]
    iv = derived[32:48]

    # Decrypt the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), 16)
    return decrypted.decode('utf-8')

def encrypt(plaintext, password):
    salt = secrets.token_bytes(8)

    derived = b""
    while len(derived) < 48:  # "key size" + "iv size" (8 + 4 magical units = 12 * 4 = 48)
        hasher = MD5.new()
        hasher.update(derived[-16:] + password.encode('utf-8') + salt)
        derived += hasher.digest()

    key = derived[0:32]
    iv = derived[32:48]

    # Encrypt the plaintext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(plaintext.encode('utf-8'), 16))

    # Combine salt and encrypted data
    encrypted_bytes = base64.b64encode(b'Salted__' + salt + encrypted)
    return encrypted_bytes.decode('utf-8')

'''
# Example
plaintext = "Hello World!"
password = "some password"
encrypted = encrypt(plaintext, password)
print("Encrypted ciphertext (base64):", encrypted)
decrypted = decrypt(encrypted, password)
print("Decrypted ciphertext (base64):", decrypted)
'''
