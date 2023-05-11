import json
import os
from base64 import b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
# link Reference: https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples
filename = 'farm'

def get_farm_file_bytes():
    if os.path.exists(filename):
        with open(filename) as farm_content:
            content_file = farm_content.read()

    # temperature
    encrypted = bytes.fromhex(content_file)
    keyDERPrivate = b64decode(PRIVATE_KEY)
    keyPrivate = RSA.importKey(keyDERPrivate)

    decryptor = PKCS1_OAEP.new(keyPrivate)
    return decryptor.decrypt(encrypted)

def get_farm_file(key_name: str):
    decrypted = get_farm_file_bytes().decode()
    return json.loads(decrypted)[key_name]


def get_databiz_queue():
    return get_farm_file("databiz_queue")


def get_path_config():
    return get_farm_file("work_folder")


PATH_MAP = "/home/conf"
RABBITMQ_HOST = "40.124.169.219"
RABBITMQ_PORT = 5672
DATABIZ_QUEUE_IDENTIFY = "databiz-identify"
PRIVATE_KEY = 'MIIEpQIBAAKCAQEAzNnqm1jK4H+vvE5gKfe/hbtdFhns8LShB9cJiQD++M0u9BKA\
/eO4HLrocZXMb8r4Nh0UqdipO5EvN9cawIg8xDgu1OYcCEd/r422Brq/miHOFwYG\
PxWryCIfg++aF2CZFynCa/OGfzFiZ0xybo+VnRX0XTbLNk4jw4kAv16VmY2PQq7u\
yAGm0WMh+V0RCjIfy3N6jntmq8waAtdNmUweGX8ALAaFEdJpbuNpBKcmYl4knWCD\
PCmWi4AYSPP0g5wrujtZXhImS/4yypYYt9p1Ks7rBo8d/DKIbDLvJcquokbqWSUh\
/azBbfdZ1s+Nrrtc3NeiXsdBtx/zeUuopC4GtwIDAQABAoIBADB2HRpDFzuk+V4C\
7J0BDz4D5TGlUHhhQvcn2AmhQrB5WfJDrmBhztx9GyBD3+lSiwXCO3Ey4FZHMnRz\
XtDNahLBd9LF3TvYLkzJqZZN96Xu+WJY+oFSDyF5cRs1Q67kG1NvfZ8sLVVJyY3G\
eAvPzAUtfHHQ1KI0OiG394VOSvXYKrVXE8Cw7fU7kjZIBES3PHX/wZCnGPFUy8iZ\
ldFcZ6rchHFSa4tj7oomYYBPmEN3RROGMjBn98cGv8vkTXhsgK0qGKukmpVY6YYT\
2uCw75c3bSFI4Jg7cjsT5+8hoK5TY+DmMd9NzxsqDqymmGmL/ZqK3lWeXeK3sTwu\
CSQ46gECgYEA1JREMKUF22lC5GI0mph0vaTbYuZ7vTq6e5l9ZnO9sEvTI+6v0RZO\
6uyofVT3BhLgYypYxWVsHBCH4+snDjOl4m3/OsubNX7h1IzMCdUhZVVO3ZUwfcRK\
M5emQY65SSicqj9fdyJpwXQeXEwdD0+c9sFzKBZ5LPpwQyVgMUPbMfECgYEA9rGO\
yV5ZVw+6qzLcd0pzIGnCxCpdjhdIFuzUP7vX/SN2xQbNYEU7NNTXIPEwYYPO/C95\
xvn5UH2iwjFZS0l08nvgFcJT9vo6xMODPU7Yfuxebbpzd0AprX2Hm9bYEf30+s/l\
lq/wmVJ20EEqWizZl2cTOYxBmzEaF4/nJsLVGycCgYEAs6ciAeJVEtrgl1aPkl9p\
uaQLbIfQ51kspKxRGDaUhttt8x4TJCcwRsX+lv0pTs7BJ81v/FL8jLNDxNDEzvHD\
LZs8ahoMb6dtf04GWgDvGk6AOi+NLZyoAPYWoazW1gcmb5LjQTGqIr3ZsrL4lCn6\
Q2e1xJlJi0OTgIujwb7RDmECgYEA8FUE/UrMkNPDENxJCnJefHpsg72eTTqDQcpR\
8RFol7XAFKzO0nY/+vVL7EzszGOj9+2sntuTNwZe1P9MtdsHcuCZ67jZIiifrmem\
6MhyhBx01kOqD8hTkjBUN89zyvt1eg+l5UrchBJhq/uAbj95cFW71fm9RJruh3vr\
Psja4ksCgYEAq2O/hfdjyPX0kD+2CYcOXv9m2Kzk0YPeBQpReJtR4Dm9xP3FLuoU\
1Gfa4z5hVTRSWOTmElv8xJtJDcTpYpx9c/R2SgMXhJlwzoYKFVlryvUJFO03JvfQ\
vghqtTTUThVqSa7OkTxOh2/CQiRMtuWvQG9GOsqp04H7/Mb7YDCAxPw='
