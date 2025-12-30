class ManuelDES:
    def __init__(self):
        self.initial_p = [
            58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
        ]
        self.final_p = [
            40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
        ]
        self.expansion_p = [
            32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23,
            24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
        ]
        self.p_table = [
            16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
            2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
        ]
        self.shift_amounts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        self.key_p_pc1 = [
            57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2,
            59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39,
            31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37,
            29, 21, 13, 5, 28, 20, 12, 4
        ]
        self.key_p_pc2 = [
            14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
            26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
        ]
        
        self.sbox = [[
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ] for _ in range(8)]

    def pad(self, data):
        padding_len = 8 - (len(data) % 8)
        return data + bytes([padding_len] * padding_len)

    def unpad(self, data):
        padding_len = data[-1]
        return data[:-padding_len]

    def bytes_to_bin(self, bytes_data):
        return ''.join(format(b, '08b') for b in bytes_data)

    def bin_to_bytes(self, bin_str):
        byte_arr = []
        for i in range(0, len(bin_str), 8):
            byte_arr.append(int(bin_str[i:i+8], 2))
        return bytes(byte_arr)

    def permute(self, input_str, table):
        return "".join([input_str[i-1] for i in table])

    def xor(self, s1, s2):
        return "".join([str(int(a) ^ int(b)) for a, b in zip(s1, s2)])

    def generate_keys(self, key_bytes):
        key_bin = self.bytes_to_bin(key_bytes)
        if len(key_bin) > 64: key_bin = key_bin[:64]
        if len(key_bin) < 64: key_bin = key_bin.ljust(64, '0')

        permuted_key = self.permute(key_bin[:64], self.key_p_pc1)
        left, right = permuted_key[:28], permuted_key[28:]
        
        keys = []
        for amt in self.shift_amounts:
            left = left[amt:] + left[:amt]
            right = right[amt:] + right[:amt]
            keys.append(self.permute(left + right, self.key_p_pc2))
        return keys

    def feistel(self, right, key):
        expanded = self.permute(right, self.expansion_p)
        xored = self.xor(expanded, key)
        output = ""
        for i in range(8):
            block = xored[i*6 : (i+1)*6]
            row = int(block[0] + block[5], 2)
            col = int(block[1:5], 2)
            val = self.sbox[i][row][col]
            output += format(val, '04b')
        return self.permute(output, self.p_table)

    def process_block(self, block_bin, round_keys, mode):
        block = self.permute(block_bin, self.initial_p)
        left, right = block[:32], block[32:]

        r_range = range(16) if mode == 'encrypt' else range(15, -1, -1)

        for i in r_range:
            old_right = right
            feistel_out = self.feistel(right, round_keys[i])
            right = self.xor(left, feistel_out)
            left = old_right
        
        final_block = right + left
        return self.permute(final_block, self.final_p)

    def encrypt(self, plain_text, key_str):
        data = plain_text.encode('utf-8')
        key_bytes = key_str.encode('utf-8')[:8]
        if len(key_bytes) < 8: key_bytes = key_bytes.ljust(8, b'\0')

        data = self.pad(data)
        round_keys = self.generate_keys(key_bytes)
        
        encrypted_bin = ""
        for i in range(0, len(data), 8):
            block_bytes = data[i:i+8]
            block_bin = self.bytes_to_bin(block_bytes)
            encrypted_bin += self.process_block(block_bin, round_keys, 'encrypt')

        return self.bin_to_bytes(encrypted_bin).decode('latin-1')

    def decrypt(self, cipher_text, key_str):
        data = cipher_text.encode('latin-1')
        key_bytes = key_str.encode('utf-8')[:8]
        if len(key_bytes) < 8: key_bytes = key_bytes.ljust(8, b'\0')
        
        round_keys = self.generate_keys(key_bytes)
        
        decrypted_bin = ""
        for i in range(0, len(data), 8):
            block_bytes = data[i:i+8]
            block_bin = self.bytes_to_bin(block_bytes)
            decrypted_bin += self.process_block(block_bin, round_keys, 'decrypt')

        decrypted_bytes = self.bin_to_bytes(decrypted_bin)
        
        try:
            return self.unpad(decrypted_bytes).decode('utf-8')
        except:
            return "Hata: DES Şifre Çözülemedi (Padding Hatası)"
