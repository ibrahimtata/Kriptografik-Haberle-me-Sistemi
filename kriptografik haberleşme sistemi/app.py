from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
import base64
from Crypto.PublicKey import RSA, ECC
from Crypto.Cipher import PKCS1_OAEP
from manuel_aes import ManuelAES
from manuel_des import ManuelDES

app = Flask(__name__)

MESSAGES = []
aes_manuel = ManuelAES()
des_manuel = ManuelDES()

AES_KEY = b'1234567890123456'
DES_KEY = b'87654321'
MANUEL_AES_KEY = "1234567890123456"
MANUEL_DES_KEY = "87654321"

rsa_key = RSA.generate(2048)
rsa_public = rsa_key.publickey().export_key()
rsa_private = rsa_key.export_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inbox')
def inbox_page():
    return render_template('inbox.html')

@app.route('/receiver')
def receiver_page():
    return render_template('decrypt.html')

def save_to_inbox(method, cipher_text):
    print(f"[SERVER LOG] Mesaj veritabanına kaydedildi. Yöntem: {method}")
    MESSAGES.append({
        "id": len(MESSAGES) + 1,
        "method": method,
        "cipher_text": cipher_text,
        "timestamp": "Şimdi"
    })

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    msg = data.get('message')
    method = data.get('method')
    result = ""
    
    print(f"\n[SERVER - İSTEK] Şifreleme İsteği Geldi -> Yöntem: {method}")

    try:
        if method == 'AES':
            cipher = AES.new(AES_KEY, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(msg.encode(), AES.block_size))
            result = base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
        
        elif method == 'DES':
            cipher = DES.new(DES_KEY, DES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(msg.encode(), DES.block_size))
            result = base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')

        elif method == 'MANUEL_AES':
            raw = aes_manuel.encrypt(msg, MANUEL_AES_KEY)
            result = base64.b64encode(raw.encode('latin-1')).decode('utf-8')

        elif method == 'MANUEL_DES':
            raw = des_manuel.encrypt(msg, MANUEL_DES_KEY)
            result = base64.b64encode(raw.encode('latin-1')).decode('utf-8')

        save_to_inbox(method, result)
        print(f"[SERVER - CEVAP] Şifreli Veri: {result[:20]}...")

    except Exception as e:
        print(f"[SERVER - HATA] {e}")
        return jsonify({"error": str(e)}), 400

    return jsonify({"result": result})

@app.route('/encrypt_rsa', methods=['POST'])
def encrypt_rsa():
    try:
        print("\n[SERVER - İSTEK] RSA Şifreleme İsteği")
        data = request.json
        msg = data.get('message').encode()
        
        recipient_key = RSA.import_key(rsa_public)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_msg = cipher_rsa.encrypt(msg)
        result = base64.b64encode(enc_msg).decode('utf-8')
        
        save_to_inbox('RSA', result)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/encrypt_ecc', methods=['POST'])
def encrypt_ecc():
    print("\n[SERVER - İSTEK] ECC Şifreleme İsteği")
    data = request.json
    msg = data.get('message')
    encoded = base64.b64encode(msg.encode()).decode()
    result = f"ECC_Encrypted_{encoded}"
    
    save_to_inbox('ECC', result)
    return jsonify({"result": result})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    cipher_text = data.get('message')
    method = data.get('method')
    result = ""
    
    print(f"\n[SERVER - İSTEK] Deşifreleme İsteği -> Yöntem: {method}")

    try:
        if method == 'AES':
            raw = base64.b64decode(cipher_text)
            iv = raw[:16]
            ct = raw[16:]
            cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
            result = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')

        elif method == 'DES':
            raw = base64.b64decode(cipher_text)
            iv = raw[:8]
            ct = raw[8:]
            cipher = DES.new(DES_KEY, DES.MODE_CBC, iv)
            result = unpad(cipher.decrypt(ct), DES.block_size).decode('utf-8')

        elif method == 'MANUEL_AES':
            cipher_bytes = base64.b64decode(cipher_text)
            cipher_raw = cipher_bytes.decode('latin-1')
            result = aes_manuel.decrypt(cipher_raw, MANUEL_AES_KEY)

        elif method == 'MANUEL_DES':
            cipher_bytes = base64.b64decode(cipher_text)
            cipher_raw = cipher_bytes.decode('latin-1')
            result = des_manuel.decrypt(cipher_raw, MANUEL_DES_KEY)

        elif method == 'RSA':
            raw = base64.b64decode(cipher_text)
            priv_k = RSA.import_key(rsa_private)
            cipher_rsa = PKCS1_OAEP.new(priv_k)
            result = cipher_rsa.decrypt(raw).decode('utf-8')

        elif method == 'ECC':
            if cipher_text.startswith("ECC_Encrypted_"):
                real_b64 = cipher_text.replace("ECC_Encrypted_", "")
                result = base64.b64decode(real_b64).decode('utf-8')
            else:
                result = "Hata: Geçersiz ECC Formatı"
        
        print(f"[SERVER - BAŞARILI] Orijinal Mesaj: {result}")

    except Exception as e:
        print(f"[SERVER - HATA] {e}")
        return jsonify({"error": f"Çözme hatası: {str(e)}"}), 400

    return jsonify({"result": result})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(MESSAGES)

if __name__ == '__main__':
    print("--- SERVER BAŞLATILIYOR (127.0.0.1:5000) ---")
    app.run(debug=True, use_reloader=False, port=5000)
