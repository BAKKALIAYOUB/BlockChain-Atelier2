import random
from sympy import mod_inverse
from math import gcd

# Fonction pour générer deux grands nombres premiers
def generate_large_primes():
    p = 61
    q = 53
    return p, q

# Génération des clés publique et privée
def generate_keys():
    p, q = generate_large_primes()
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choisir e tel que 1 < e < phi et pgcd(e, phi) = 1
    e = random.choice([i for i in range(2, phi) if gcd(i, phi) == 1])
    
    # Calcul de d (inverse modulaire de e modulo phi)
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)

# Chiffrement RSA de base
def encrypt_rsa(m, public_key):
    e, n = public_key
    return pow(m, e, n)

# Déchiffrement RSA de base
def decrypt_rsa(c, private_key):
    d, n = private_key
    return pow(c, d, n)

# Fonction de permutation (exemple simple : inversement des bits)
def bit_permutation(value):
    return int('{:016b}'.format(value)[::-1], 2)

# Fonction inverse de permutation
def inverse_bit_permutation(value):
    return bit_permutation(value)  # Symétrique dans cet exemple

# Chiffrement avec permutation
def encrypt_with_permutation(message, public_key):
    # Chiffrement RSA de base
    encrypted_message = encrypt_rsa(message, public_key)
    # Appliquer la permutation des bits
    permuted_message = bit_permutation(encrypted_message)
    return permuted_message

# Déchiffrement avec permutation
def decrypt_with_permutation(encrypted_message, private_key):
    # Inverser la permutation
    decrypted_permuted_message = inverse_bit_permutation(encrypted_message)
    # Déchiffrement RSA de base
    decrypted_message = decrypt_rsa(decrypted_permuted_message, private_key)
    return decrypted_message

# Fonction principale pour tester
def main():
    # Génération des clés
    public_key, private_key = generate_keys()
    
    print("Clé publique :", public_key)
    print("Clé privée :", private_key)

    # Message à chiffrer (doit être inférieur à n)
    message = 123
    print("Message original :", message)
    
    # Chiffrement
    encrypted_message = encrypt_with_permutation(message, public_key)
    print("Message chiffré :", encrypted_message)
    
    # Déchiffrement
    decrypted_message = decrypt_with_permutation(encrypted_message, private_key)
    print("Message déchiffré :", decrypted_message)

if __name__ == "__main__":
    main()
