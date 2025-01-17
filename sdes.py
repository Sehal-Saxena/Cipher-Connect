# sdes.py
import random
import string

class SDES:
    def __init__(self):
        self.key = self.generate_random_key()
        self.subkeys = self.generate_subkeys(self.key)
    
    def generate_random_key(self):
        # Generate a random 10-bit key
        return ''.join(random.choice('01') for _ in range(10))
    
    def permute(self, data, table):
        return ''.join(data[i - 1] for i in table)
    
    def generate_subkeys(self, key):
        # Initial Permutation 10
        P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        # Permutation 8
        P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        
        # Apply P10
        key = self.permute(key, P10)
        left = key[:5]
        right = key[5:]
        
        # Generate first key (left shift 1)
        left = left[1:] + left[0]
        right = right[1:] + right[0]
        k1 = self.permute(left + right, P8)
        
        # Generate second key (left shift 2)
        left = left[2:] + left[:2]
        right = right[2:] + right[:2]
        k2 = self.permute(left + right, P8)
        
        return (k1, k2)
    
    def f_function(self, right, subkey):
        # Expansion permutation
        EP = [4, 1, 2, 3, 2, 3, 4, 1]
        expanded = self.permute(right, EP)
        
        # XOR with subkey
        xored = ''.join(str(int(a) ^ int(b)) for a, b in zip(expanded, subkey))
        
        # S-boxes
        S0 = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 3, 2]
        ]
        S1 = [
            [0, 1, 2, 3],
            [2, 0, 1, 3],
            [3, 0, 1, 0],
            [2, 1, 0, 3]
        ]
        
        # Apply S-boxes
        s0_in = xored[:4]
        s1_in = xored[4:]
        row0 = int(s0_in[0] + s0_in[3], 2)
        col0 = int(s0_in[1:3], 2)
        row1 = int(s1_in[0] + s1_in[3], 2)
        col1 = int(s1_in[1:3], 2)
        
        s0_out = format(S0[row0][col0], '02b')
        s1_out = format(S1[row1][col1], '02b')
        
        # P4 permutation
        P4 = [2, 4, 3, 1]
        return self.permute(s0_out + s1_out, P4)
    
    def encrypt_text(self, text):
        # Convert text to binary
        binary = ''.join(format(ord(c), '08b') for c in text)
        # Pad if necessary
        if len(binary) % 8 != 0:
            binary += '0' * (8 - (len(binary) % 8))
        
        # Encrypt each 8-bit block
        encrypted = ''
        for i in range(0, len(binary), 8):
            block = binary[i:i+8]
            encrypted += self.encrypt(block)
        return encrypted
    
    def decrypt_text(self, binary):
        # Decrypt each 8-bit block
        decrypted_binary = ''
        for i in range(0, len(binary), 8):
            block = binary[i:i+8]
            decrypted_binary += self.decrypt(block)
        
        # Convert binary back to text
        text = ''
        for i in range(0, len(decrypted_binary), 8):
            byte = decrypted_binary[i:i+8]
            text += chr(int(byte, 2))
        return text
    
    def encrypt(self, plaintext):
        # Initial Permutation
        IP = [2, 6, 3, 1, 4, 8, 5, 7]
        text = self.permute(plaintext, IP)
        
        left = text[:4]
        right = text[4:]
        
        # First round
        temp = self.f_function(right, self.subkeys[0])
        new_left = ''.join(str(int(a) ^ int(b)) for a, b in zip(left, temp))
        new_right = right
        
        # Second round
        temp = self.f_function(new_left, self.subkeys[1])
        final_right = ''.join(str(int(a) ^ int(b)) for a, b in zip(new_right, temp))
        final_left = new_left
        
        # Final Permutation
        IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
        return self.permute(final_right + final_left, IP_inv)
    
    def decrypt(self, ciphertext):
        # Initial Permutation
        IP = [2, 6, 3, 1, 4, 8, 5, 7]
        text = self.permute(ciphertext, IP)
        
        left = text[:4]
        right = text[4:]
        
        # First round (with second subkey)
        temp = self.f_function(right, self.subkeys[1])
        new_left = ''.join(str(int(a) ^ int(b)) for a, b in zip(left, temp))
        new_right = right
        
        # Second round (with first subkey)
        temp = self.f_function(new_left, self.subkeys[0])
        final_right = ''.join(str(int(a) ^ int(b)) for a, b in zip(new_right, temp))
        final_left = new_left
        
        # Final Permutation
        IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
        return self.permute(final_right + final_left, IP_inv)