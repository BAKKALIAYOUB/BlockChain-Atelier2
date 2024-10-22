import random
from sympy import mod_inverse
from math import gcd

def is_prime(n, k=5):
    """Test if a number is prime using Miller-Rabin primality test"""
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
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

def generate_large_prime(bits=512):
    """Generate a prime number with specified number of bits"""
    while True:
        n = random.getrandbits(bits) | (1 << bits - 1) | 1
        if is_prime(n):
            return n

def generate_large_primes(bits=512):
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
    
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)
    
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def string_to_blocks(message, block_size):
    """Convert string to blocks of numbers"""
    # Convert string to bytes then to integer blocks
    message_bytes = message.encode('utf-8')
    blocks = []
    current_block = 0
    bit_count = 0
    
    for byte in message_bytes:
        current_block = (current_block << 8) | byte
        bit_count += 8
        
        if bit_count >= block_size * 8:
            blocks.append(current_block)
            current_block = 0
            bit_count = 0
    
    # Add any remaining bits as the last block
    if bit_count > 0:
        blocks.append(current_block)
    
    return blocks

def blocks_to_string(blocks, block_size):
    """Convert blocks of numbers back to string"""
    message_bytes = bytearray()
    
    for block in blocks:
        # Convert block to bytes
        block_bytes = block.to_bytes((block.bit_length() + 7) // 8, byteorder='big')
        message_bytes.extend(block_bytes)
    
    # Remove padding and convert to string
    try:
        return message_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # If there's padding, trim it off
        while message_bytes and message_bytes[-1] == 0:
            message_bytes = message_bytes[:-1]
        return message_bytes.decode('utf-8')

def encrypt_block(block, public_key):
    """Encrypt a single block"""
    e, n = public_key
    return pow(block, e, n)

def decrypt_block(block, private_key):
    """Decrypt a single block"""
    d, n = private_key
    return pow(block, d, n)

def encrypt_string(message, public_key):
    """Encrypt a string message"""
    e, n = public_key
    # Calculate maximum block size (in bytes) based on key size
    block_size = (n.bit_length() - 1) // 8 - 1  # Leave room for padding
    
    # Convert string to blocks
    blocks = string_to_blocks(message, block_size)
    
    # Encrypt each block
    encrypted_blocks = [encrypt_block(block, public_key) for block in blocks]
    
    return encrypted_blocks

def decrypt_string(encrypted_blocks, private_key):
    """Decrypt encrypted blocks back to string"""
    d, n = private_key
    block_size = (n.bit_length() - 1) // 8 - 1
    
    # Decrypt each block
    decrypted_blocks = [decrypt_block(block, private_key) for block in encrypted_blocks]
    
    # Convert blocks back to string
    return blocks_to_string(decrypted_blocks, block_size)

def main():
    # Generate keys
    public_key, private_key = generate_keys()
    print("Public key:", public_key)
    print("Private key:", private_key)
    
    # Test message
    message = "Hi my Name is AYoub"
    print("\nOriginal message:", message)
    
    # Encryption
    encrypted_blocks = encrypt_string(message, public_key)
    print("Encrypted blocks:", encrypted_blocks)
    
    # Decryption
    decrypted_message = decrypt_string(encrypted_blocks, private_key)
    print("Decrypted message:", decrypted_message)
    
    # Verify
    print("\nDecryption successful:", message == decrypted_message)

if __name__ == "__main__":
    main()