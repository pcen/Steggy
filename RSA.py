from os.path import exists
from Crypto.PublicKey import RSA

# abstraction of RSA encryption
# RSA keys are loaded in .pem files specified by file-path strings
class RSAService:

    PRIV_PEM = 'private.pem'
    PUB_PEM = 'public.pem'

    def __init__(self, priv_pem = None, pub_pem = None):
        if pub_pem is not None:
            self.PUB_PEM = pub_pem
        elif priv_pem is not None:
            self.PRIV_PEM = priv_pem
            self.generate_RSA()
        elif exists(self.PRIV_PEM):
            pass
        else:
            self.generate_RSA()

        self.public = self.load_public()
        self.private = self.load_private()

    def generate_RSA(self):
        try:
            private = RSA.generate(2048)
            self.export_key(private, self.PRIV_PEM)
            self.export_key(private.publickey(), self.PUB_PEM)
            return True
        except:
            print('Failed to generate RSA key-pair.')
        return False

    def export_key(self, key, pem):
        try:
            f = open(pem, 'wb')
            f.write(key.exportKey())
            f.close()
            return True
        except:
            return False

    def load_key(self, pem):
        try:
            f = open(pem)
            key = RSA.importKey(f.read())
            f.close()
            return key
        except:
            return None

    def load_private(self):
        private_key = self.load_key(self.PRIV_PEM)
        if private_key is None:
            print('Failed to load RSA private key.')
            return None
        return private_key

    def load_public(self, pem = None):
        if pem is None:
            pem = self.PUB_PEM
        public_key = self.load_key(pem)
        if public_key is None:
            print('Failed to load RSA public key.')
            return None
        return public_key

    def public_encrypt(self, public_pem, plain_text):
        public = self.load_public(pem = public_pem)
        self.plain_text = plain_text
        self.cipher_text = public.encrypt(plain_text, 0)
        return self.cipher_text

    def encrypt(self, plain_text):
        self.plain_text = plain_text
        self.cipher_text = self.private.encrypt(plain_text, 0)
        return self.cipher_text

    def decrypt(self, cipher_text):
        self.decrypted_text = self.private.decrypt(cipher_text)
        return self.decrypted_text
