class ManuelAES:
    def __init__(self):
        self.sbox = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
            0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76
        ]

    def sub_bytes(self, state):
        return [self.sbox[b % 16] for b in state]

    def shift_rows(self, state):
        if len(state) < 2: return state
        return state[1:] + state[:1]

    def add_round_key(self, state, key):
        return [s ^ ord(key[i % len(key)]) for i, s in enumerate(state)]

    def encrypt(self, plain_text, key):
        state = [ord(c) for c in plain_text]
        
        state = self.add_round_key(state, key)
        
        state = self.sub_bytes(state)
        
        state = self.shift_rows(state)
        

        return "".join([chr(b) for b in state])

