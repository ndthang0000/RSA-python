import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw,AES.block_size)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

a=AESCipher('thang nguyen')
encrypt_message=a.encrypt('nguyen duc thang')
print(encrypt_message)
