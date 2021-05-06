from hashlib import sha256

from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA

def _pad(s, bs):
    return s + (bs - len(s.encode('utf-8')) % bs) * chr(bs - len(s.encode('utf-8')) % bs)  # 필요한 바이트 만큼 붙여줌

def _unpad(s):
    return s[ : -ord( s[ len(s)-1 : ] ) ]  # pad 함수로 padding 된 s를 원상복귀 시킴

def aes(origin):
    print("\ncipher type(DES/DES3/AES/ARS4): AES")

    while True:
        key = input("key(16/24/32): ").encode('utf-8')
        if len(key) not in (16, 24, 32):
            print("check key's length, input key's length should be (16,24,32)")
        else:
            break

    bs = AES.block_size  # bs(block size) : 16 byte
    iv = Random.new().read(bs)  # initial vector : 16 byte
    string = _pad(origin, bs)  #padding 함

    # encrypt
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    cipher_text = iv + cipher.encrypt(string.encode('utf-8'))
    print(f"encrypted: {cipher_text}")

    # decrypt
    iv = cipher_text[:AES.block_size]

    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    plain_text = _unpad(cipher.decrypt(cipher_text[AES.block_size:])).decode('utf-8')
    print(f"decrypted: {plain_text}")

def sha(origin):
    print("\nhash type(SHA/SHA256/SHA384/SHA512/HMAC): SHA256")
    result = sha256(origin.encode('utf-8')).hexdigest()
    print(result)

def rsa(origin):
    print("\nRSA")

    while True:
        key_length: int = int(input("key length(x256, >=1024): "))
        if key_length < 1024 or (key_length % 256) != 0:
            print("key length should longer than 1024 and should divisible with 256")
        else:
            break

    key = RSA.generate(key_length)  # random key generate

    private_key = key.exportKey('DER')  
    public_key = key.publickey().exportKey('DER')  

    private_key = RSA.importKey(private_key)  
    public_key = RSA.importKey(public_key) 

    encrypt = PKCS1_v1_5.new(public_key)
    cipher_text = encrypt.encrypt(origin.encode('utf-8'))
    print(f"encrypted: {cipher_text}")

    decrypt = PKCS1_v1_5.new(private_key)
    plaintext = decrypt.decrypt(cipher_text, sentinel=None).decode()
    print(f"decrypted: {plaintext}")


origin = input("original data: ")

aes(origin)
sha(origin)
rsa(origin)