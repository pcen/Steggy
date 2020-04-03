from Steggy.cryptography.RSA import RSAService
from Steggy.cryptography.AES import AESService

# encryption service enforcing encryption of AES symmetric key with RSA
class CryptoService:

    def __init__(self):
        self.aes = AESService()
        self.aes_key = self.aes.key
        self.rsa = RSAService()
        self.encrypted_aes_key = self.rsa.encrypt(self.aes_key)

    def encrypt(self, plain_text):
        self.cipher = self.aes.encrypt(plain_text)
        return (self.encrypted_aes_key, self.cipher)

    def decrypt(self, encrypted_key, cipher_text):
        aes_key = self.rsa.decrypt(encrypted_key)
        decryptor = AESService(key = aes_key)
        self.decrypted_pt = decryptor.decrypt(cipher_text)
        return self.decrypted_pt
