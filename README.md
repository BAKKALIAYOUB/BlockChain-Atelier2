# Enhanced RSA Encryption with Bit Permutation

## Overview
This implementation provides a secure encryption system combining the RSA (Rivest-Shamir-Adleman) algorithm with an additional layer of security through bit permutation. The combination of these two techniques offers enhanced protection against certain types of cryptographic attacks.

## Table of Contents
- [RSA Algorithm](#rsa-algorithm)
- [Bit Permutation Enhancement](#bit-permutation-enhancement)
- [Implementation Details](#implementation-details)
- [Usage](#usage)
- [Security Considerations](#security-considerations)

## RSA Algorithm
RSA is an asymmetric cryptographic algorithm based on the mathematical properties of large prime numbers. The security of RSA relies on the practical difficulty of factoring the product of two large prime numbers.

### Key Components:
1. **Key Generation**:
   - Two prime numbers (p, q) are selected
   - Calculate n = p * q
   - Calculate φ(n) = (p-1) * (q-1)
   - Choose public exponent e where 1 < e < φ(n) and gcd(e, φ(n)) = 1
   - Calculate private exponent d = e^(-1) mod φ(n)

2. **Encryption**:
   - For a message m, the encrypted text c = m^e mod n

3. **Decryption**:
   - For an encrypted message c, the original message m = c^d mod n

## Bit Permutation Enhancement
This implementation adds an extra security layer through bit permutation after the RSA encryption process.

### How it works:
1. After RSA encryption, the ciphertext undergoes a bit permutation
2. The bits of the encrypted message are rearranged according to a predefined pattern
3. This adds complexity to the ciphertext and provides additional protection against certain types of attacks

## Implementation Details

### Key Functions:
```python
def generate_keys()
# Generates public and private key pairs

def encrypt_with_permutation(message, public_key)
# Encrypts message using RSA and applies bit permutation

def decrypt_with_permutation(encrypted_message, private_key)
# Reverses bit permutation and decrypts using RSA
```

### Security Parameters:
- Prime numbers p = 61 and q = 53
- 16-bit permutation (can be extended for larger numbers)
- Random public exponent e selected for each key generation

## Usage

```python
# Generate key pairs
public_key, private_key = generate_keys()

# Encrypt a message
message = 123
encrypted_message = encrypt_with_permutation(message, public_key)

# Decrypt the message
decrypted_message = decrypt_with_permutation(encrypted_message, private_key)
```

## Security Considerations

1. **Prime Numbers**:
   - Current implementation uses small primes (61, 53) for demonstration
   - Production use requires much larger prime numbers (2048+ bits)

2. **Bit Permutation**:
   - Current implementation uses 16-bit permutation
   - Can be enhanced with more complex permutation patterns
   - Consider implementing dynamic permutation patterns

3. **Limitations**:
   - Message size must be smaller than n (p * q)
   - Current implementation is not suitable for large messages
   - No padding scheme implemented

