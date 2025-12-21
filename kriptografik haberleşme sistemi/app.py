from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from manuel_aes import ManuelAES  
from manuel_des import ManuelDES  

app = Flask(__name__)

aes_manuel_isleyici = ManuelAES()
des_manuel_isleyici = ManuelDES()

AES_KEY = b'1234567890123456' 
DES_KEY = b'87654321'         

key_pair = RSA.generate(2048)
public_key = key_pair.publickey().export_key()
private_key = key_pair.export_key()

@app.route('/get_public_key', methods=['GET'])
def get_public_key():
    return jsonify({"public_key": public_key.decode('utf-8')})

@app.route('/encrypt_rsa', methods=['POST'])
def encrypt_rsa():
    data = request.json
    msg = data.get('message').encode()
    
    recipient_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_msg = cipher_rsa.encrypt(msg)
    
    return jsonify({"result": base64.b64encode(encrypted_msg).decode('utf-8')})


def manuel_des_simple(text, key):
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    msg = data.get('message')
    method = data.get('method')
    
    if method == 'AES':
        cipher = AES.new(AES_KEY, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(msg.encode(), AES.block_size))
        result = base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
        
    elif method == 'DES':
        cipher = DES.new(DES_KEY, DES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(msg.encode(), DES.block_size))
        result = base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
        
    elif method == 'MANUEL_DES':
        encrypted_raw = des_manuel_isleyici.encrypt(msg, "87654321")
        result = base64.b64encode(encrypted_raw.encode('latin-1', errors='ignore')).decode('utf-8')
        
    elif method == 'MANUEL_AES':
        sifreli_ham = aes_manuel_isleyici.encrypt(msg, "1234567890123456")
        result = base64.b64encode(sifreli_ham.encode('latin-1')).decode('utf-8')
        
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
