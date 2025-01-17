import math
import random

class RSA:
    def __init__(self):
        self.public_key, self.private_key = self.generate_keypair()
    
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_prime(self):
        # Generate a random prime number between 100 and 1000
        while True:
            num = random.randint(100, 1000)
            if self.is_prime(num):
                return num
    
    def generate_keypair(self):
        p = self.generate_prime()
        q = self.generate_prime()
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # Choose public key e
        e = 65537  # Commonly used value for e
        
        # Calculate private key d
        d = pow(e, -1, phi)
        
        return ((e, n), (d, n))
    
    def encrypt(self, message, public_key):
        e, n = public_key
        message_int = int.from_bytes(message.encode(), 'big')
        cipher = pow(message_int, e, n)
        return cipher
    
    def decrypt(self, cipher):
        d, n = self.private_key
        message_int = pow(cipher, d, n)
        message = message_int.to_bytes((message_int.bit_length() + 7) // 8, 'big').decode()
        return message
