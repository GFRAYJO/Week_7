import requests
import json
import base64

SERVER_HOST = 'localhost:9500'
CA_HOST = 'localhost:9500'

def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string.encode())

server_name = requests.get(SERVER_HOST).text

server_key = requests.get(CA_HOST, params={'server_name': server_name})

cipher_text = encode(server_key.text, 'session cipher key')

result = requests.post(SERVER_HOST, json={'cipher_text': cipher_text.decode()})

print(result.text)
