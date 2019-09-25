from Crypto.Cipher import AES
from Crypto import Random

# pad plain text a length divisible by 16
def PKCS7_pad(plain_text):
    if isinstance(plain_text, str):
        plain_text = plain_text.encode('utf-8')
    length = AES.block_size - len(plain_text) % AES.block_size
    return plain_text + (chr(length) * length).encode()

# unpad plain text after decrypting cipher
def PKCS7_depad(plain_bytes):
    padding_length = plain_bytes[-1]
    plain_bytes = plain_bytes[:-padding_length]
    return plain_bytes.decode()

# abstraction of AES CBC encryption
class AESService:
    
    len_iv = AES.block_size

    def __init__(self, key = None):
        if key is None:
            self.key = Random.new().read(32)
        else:
            self.key = key
        self.mode = AES.MODE_CBC

    def CKPS7_depad(self, plain_text):
        return plain_text

    def iv(self):
        return Random.new().read(self.len_iv)

    def encrypt(self, plain_text, key = None):
        self.plain_text = PKCS7_pad(plain_text)
        if key is None:
            key = self.key
        iv = self.iv()
        cipher = AES.new(key, self.mode, iv)
        self.cipher_text = iv + cipher.encrypt(self.plain_text)
        return self.cipher_text

    def decrypt(self, cipher_text, key = None):
        if key is None:
            key = self.key
        self.cipher_text = cipher_text
        cipher = AES.new(key, self.mode, cipher_text[:self.len_iv])
        pt = cipher.decrypt(cipher_text)[self.len_iv:]
        self.decrypted_pt = PKCS7_depad(pt)
        return self.decrypted_pt
