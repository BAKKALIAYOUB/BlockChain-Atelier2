import random
from sympy import mod_inverse
from math import gcd

def is_prime(n, k=5):
    """Test if a number is prime using Miller-Rabin primality test"""
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits=200):
    """Generate a prime number with specified number of bits"""
    while True:
        # Generate random odd number with specified bits
        n = random.getrandbits(bits) | (1 << bits - 1) | 1
        if is_prime(n):
            return n

def generate_large_primes(bits=200):
    """Generate two different large prime numbers"""
    p = generate_large_prime(bits)
    while True:
        q = generate_large_prime(bits)
        if q != p:
            return p, q

def generate_keys():
    """Generate public and private key pairs"""
    p, q = generate_large_primes()
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Common choices for e are 65537 (2^16 + 1) as it's large enough and has few 1s in binary
    e = 65537
    
    # Ensure e and phi are coprime
    while gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)
    
    # Calculate private key
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def encrypt_rsa(m, public_key):
    """Basic RSA encryption"""
    e, n = public_key
    return pow(m, e, n)

def decrypt_rsa(c, private_key):
    """Basic RSA decryption"""
    d, n = private_key
    return pow(c, d, n)

def bit_permutation(value, bits=512):
    """Permute bits (more sophisticated than simple reverse)"""
    binary = format(value, f'0{bits}b')
    # More complex permutation pattern
    permuted = ''.join(binary[i] for i in range(len(binary)-1, -1, -2)) + \
               ''.join(binary[i] for i in range(len(binary)-2, -1, -2))
    return int(permuted, 2)

def inverse_bit_permutation(value, bits=512):
    """Inverse of the bit permutation"""
    binary = format(value, f'0{bits}b')
    half_len = bits // 2
    # Reconstruct original from permutation pattern
    original = ['0'] * bits
    j = 0
    for i in range(bits-1, -1, -2):
        original[i] = binary[j]
        j += 1
    for i in range(bits-2, -1, -2):
        original[i] = binary[j]
        j += 1
    return int(''.join(original), 2)

def encrypt_with_permutation(message, public_key):
    """Encrypt message with RSA and bit permutation"""
    encrypted_message = encrypt_rsa(message, public_key)
    permuted_message = bit_permutation(encrypted_message)
    return permuted_message

def decrypt_with_permutation(encrypted_message, private_key):
    """Decrypt message with inverse permutation and RSA"""
    decrypted_permuted_message = inverse_bit_permutation(encrypted_message)
    decrypted_message = decrypt_rsa(decrypted_permuted_message, private_key)
    return decrypted_message

def main():
    # Generate keys
    public_key, private_key = generate_keys()
    print("Public key:", public_key)
    print("Private key:", private_key)
    
    # Message to encrypt (must be less than n)
    message = "Ajna"
    print("\nOriginal message:", message)
    
    # Encryption
    encrypted_message = encrypt_with_permutation(message, public_key)
    print("Encrypted message:", encrypted_message)
    
    # Decryption
    decrypted_message = decrypt_with_permutation(encrypted_message, private_key)
    print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    main()