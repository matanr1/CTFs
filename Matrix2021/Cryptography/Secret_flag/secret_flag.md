# Secret


After Some googling I found that it's shamir share key  - https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing

Lets find the shared key
```python
from secretsharing import SecretSharer
d = {'Entity_1': '9362e50f3be0a411a75b55086b9b34f796dbeef58c498edcc185e3a3dc0bf905',
     'Entity_2': 'c58c3821a12d58e854922d0b3856ebf01692bbca7b9637cebb4e2cc6934859c',
     'Entity_3': '6ae19b589a96947699c96958d7bead57315fecd84cec3c3a4958a316b263575b',
     'Entity_4': 'aefd6c92bd6be0c9e4dc28a0d846f0c026c032487be21914da712482b7986d19',
     'Entity_5': 'd8ac37308292ba88668160a8b51e38f9e189fc0d349afa0c9efe671078d3c6d6'}
shares= [f"1-{d['Entity_1']}",f"2-{d['Entity_2']}",f"3-{d['Entity_3']}"]
k = SecretSharer.recover_secret(shares[0:3])
print(k)
```

`Shared Key = f1b83682fa9cbe59cacba59d0ae9af44`

After getting the IV from the web -> `985246f1480134f60eeeb9e8c2d08910` we need to decrypt the text file
```python
from Crypto.Cipher import AES
import binascii

keyBinary = binascii.unhexlify('f1b83682fa9cbe59cacba59d0ae9af44')
ivBinary = binascii.unhexlify('985246f1480134f60eeeb9e8c2d08910')
with open('enc.txt','rb') as f:
     ciphertextBinary = f.read()
# Decryption
decrypter = AES.new(keyBinary, AES.MODE_CBC, ivBinary)
plaintextBinary = decrypter.decrypt(ciphertextBinary)
plaintext = plaintextBinary.decode('utf-8')
print(plaintext)
```

Result:
`MCL{Sh4m1r's_S3c73t_Sh4r1n9_$$$}`


