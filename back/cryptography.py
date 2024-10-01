import math
import random
import os
import tempfile

# Inicia variáveis globais para armazenar os caminhos dos arquivos temporários
CAMINHO_CHAVE_PUB = None
CAMINHO_CHAVE_PRIV = None
CAMINHO_CANAL = None

# Função que encontra todos os números primos até 250, isso por meio da Sifra de Eratóstenes
# Funcionamento: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
def encontrar_num_primos():
    sifra = [True] * 250
    sifra[0] = sifra[1] = False
    for i in range(2, int(math.sqrt(250)) + 1):
        if sifra[i]:
            for j in range(i * i, 250, i):
                sifra[j] = False
    primos = [i for i, eh_primo in enumerate(sifra) if eh_primo]
    return primos

# Retorna um número aleatório
def primo_aleatorio(primos):
    return random.choice(primos)

# Geração das chaves e carregamento em seus respectivos arquivos
def gerar_chaves():
    global CAMINHO_CHAVE_PUB, CAMINHO_CHAVE_PRIV, CAMINHO_CANAL

    # Encontrar dois primos aleatórios
    primos = encontrar_num_primos()
    primeiro_primo_aleatorio = primo_aleatorio(primos)
    segundo_primo_aleatorio = primo_aleatorio(primos)

    # Garante que os primos são diferentes
    while primeiro_primo_aleatorio == segundo_primo_aleatorio:
        segundo_primo_aleatorio = primo_aleatorio(primos)

    # Calcula n como o produto dos dois primos
    n = primeiro_primo_aleatorio * segundo_primo_aleatorio

    # Calcula a função totiente de Euler, φ(n)
    # φ(n) = (p - 1) * (q - 1), onde p e q são primos
    fi = (primeiro_primo_aleatorio - 1) * (segundo_primo_aleatorio - 1)

    # Encontrar e que seja coprimo com φ(n)
    chave_publica = random.choice([i for i in range(2, fi) if math.gcd(i, fi) == 1])

    # Encontrar d tal que (d * e) % φ(n) == 1
    chave_privada = pow(chave_publica, -1, fi)

    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as public_key_file, \
            tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as private_key_file, \
            tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as n_file:

        CAMINHO_CHAVE_PUB = public_key_file.name
        CAMINHO_CHAVE_PRIV = private_key_file.name
        CAMINHO_CANAL = n_file.name

        # Escreva as chaves nos arquivos temporários
        public_key_file.write(str(chave_publica))
        private_key_file.write(str(chave_privada))
        n_file.write(str(n))

def load_keys():
    global CAMINHO_CHAVE_PUB, CAMINHO_CHAVE_PRIV, CAMINHO_CANAL

    try:
        if not (CAMINHO_CHAVE_PUB and CAMINHO_CHAVE_PRIV and CAMINHO_CANAL):
            gerar_chaves()

        with open(CAMINHO_CHAVE_PUB, 'r') as file:
            public_key = int(file.read())
        with open(CAMINHO_CHAVE_PRIV, 'r') as file2:
            private_key = int(file2.read())
        with open(CAMINHO_CANAL, 'r') as file3:
            n = int(file3.read())

        os.remove(CAMINHO_CHAVE_PUB)
        os.remove(CAMINHO_CHAVE_PRIV)
        os.remove(CAMINHO_CANAL)

        CAMINHO_CHAVE_PUB = None
        CAMINHO_CHAVE_PRIV = None
        CAMINHO_CANAL = None

        return public_key, private_key, n
    except FileNotFoundError:
        gerar_chaves()
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