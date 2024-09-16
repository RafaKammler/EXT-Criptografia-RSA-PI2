import math
import random
import os
import tempfile

# Utiliza variáveis globais para armazenar os caminhos dos arquivos temporários
PUBLIC_KEY_PATH = None
PRIVATE_KEY_PATH = None
N_PATH = None

def ensure_directory_exists(filepath):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

def primefiller():
    sieve = [True] * 250
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(250)) + 1):
        if sieve[i]:
            for j in range(i * i, 250, i):
                sieve[j] = False
    primes = [i for i, is_prime in enumerate(sieve) if is_prime]
    return primes

def pickrandomprime(primes):
    return random.choice(primes)

def generate_keys():
    primes = primefiller()
    prime1 = pickrandomprime(primes) 
    prime2 = pickrandomprime(primes)
    
    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)
    
    # Encontrar e que seja coprimo com fi
    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1

    public_key = e
    
    # Encontrar d tal que (d * e) % fi == 1
    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1

    private_key = d

    # Criação de arquivos temporários para armazenar as chaves
    global PUBLIC_KEY_PATH, PRIVATE_KEY_PATH, N_PATH

    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as public_key_file, \
         tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as private_key_file, \
         tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as n_file:

        PUBLIC_KEY_PATH = public_key_file.name
        PRIVATE_KEY_PATH = private_key_file.name
        N_PATH = n_file.name

        # Escreva as chaves nos arquivos temporários
        public_key_file.write(str(public_key))
        private_key_file.write(str(private_key))
        n_file.write(str(n))

def load_keys():
    global PUBLIC_KEY_PATH, PRIVATE_KEY_PATH, N_PATH

    try:
        if not (PUBLIC_KEY_PATH and PRIVATE_KEY_PATH and N_PATH):
            generate_keys()

        with open(PUBLIC_KEY_PATH, 'r') as file:
            public_key = int(file.read())
        with open(PRIVATE_KEY_PATH, 'r') as file2:
            private_key = int(file2.read())
        with open(N_PATH, 'r') as file3:
            n = int(file3.read())

        # Remova os arquivos temporários após o uso
        os.remove(PUBLIC_KEY_PATH)
        os.remove(PRIVATE_KEY_PATH)
        os.remove(N_PATH)

        # Limpeza das variáveis globais
        PUBLIC_KEY_PATH = None
        PRIVATE_KEY_PATH = None
        N_PATH = None

        return public_key, private_key, n
    except FileNotFoundError:
        generate_keys()
        return load_keys()

def mod_exp(base, exp, mod):
    base = int(base)
    mod = int(mod)
    result = 1
    base = base % mod
    while exp > 0:
        if (exp % 2) == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def encrypt(message, public_key, n):
    return mod_exp(message, public_key, n)

def decrypt(encrypted_text, private_key, n):
    return mod_exp(encrypted_text, private_key, n)

def encoder(message, public_key, n):
    encoded = []
    for letter in message:
        encoded.append(encrypt(ord(letter), public_key, n))
    return encoded

def decoder(encoded, private_key, n):
    decoded = ''
    for num in encoded:
        decoded += chr(decrypt(num, private_key, n))
    return decoded

def undo_joined_message(joined_message):
    return [int(p) for p in joined_message.split()]


