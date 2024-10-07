import math
import random



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


# Retorna um número aleatório da lista
def primo_aleatorio(primos):
    return random.choice(primos)


# Geração das chaves e carregamento em seus respectivos arquivos
def gerar_chaves():

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

    return chave_publica, chave_privada, n

# Realiza a operação de exponenciação modular de maneira eficiente
# Calculando (base^exp) % mod
def expo_modular(base, exp, mod):

    # Converte base e mod para inteiros, inicializa o resultado e reduz a base
    base = int(base)
    mod = int(mod)
    resultado = 1
    base = base % mod

    # Enquanto exp for maior que 0:
    # Se exp for ímpar, então resultado = (resultado * base) % mod
    # E exp = exp / 2, base = (base * base) % mod
    while exp > 0:
        if (exp % 2) == 1:
            resultado = (resultado * base) % mod
        exp = exp >> 1
        base = (base * base) % mod

    return resultado

# Funções que criptografam e descriptografam as mensagens______________________________________________________________


def criptografar(mensagem, chave_publica, canal):
    return expo_modular(mensagem, chave_publica, canal)

def descriptografar(texto_criptografado, chave_privada, canal):
    return expo_modular(texto_criptografado, chave_privada, canal)

def codificar_msg(mensagem, chave_publica, canal):
    msg_codificada = []

    # Converte cada letra da mensagem em seu valor ASCII e criptografa
    for letra in mensagem:
        msg_codificada.append(criptografar(ord(letra), chave_publica, canal))

    return msg_codificada

def decodificar(msg_codificada, chave_privada, canal):
    msg_decodificada = ''

    # Descriptografa cada número da mensagem e converte para letra
    for num in msg_codificada:
        msg_decodificada += chr(descriptografar(num, chave_privada, canal))

    return msg_decodificada

def separar_msg(mensagem_junta):
    return [int(p) for p in mensagem_junta.split()]