import math
import random


# Inicia a classe para criptografia RSA
class CriptografiaRSA:
    def __init__(self):
        self.primos = []
        self.encontrar_num_primos()

    # Função que encontra todos os números primos até 250, isso por meio da Sifra de Eratóstenes
    # Funcionamento: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    def encontrar_num_primos(self):
        sifra = [True] * 250
        sifra[0] = sifra[1] = False
        for i in range(2, int(math.sqrt(250)) + 1):
            if sifra[i]:
                for j in range(i * i, 250, i):
                    sifra[j] = False
        self.primos = [i for i, eh_primo in enumerate(sifra) if eh_primo]



    # Retorna um número aleatório da lista
    def primo_aleatorio(self):
        return random.choice(self.primos)


    # Geração das chaves e carregamento em seus respectivos arquivos
    def gerar_chaves(self):

        # Encontrar dois primos aleatórios
        primeiro_primo_aleatorio = self.primo_aleatorio()
        segundo_primo_aleatorio = self.primo_aleatorio()

        # Garante que os primos são diferentes
        while primeiro_primo_aleatorio == segundo_primo_aleatorio:
            segundo_primo_aleatorio = self.primo_aleatorio()

        # Calcula n como o produto dos dois primos
        n = primeiro_primo_aleatorio * segundo_primo_aleatorio

        # Calcula a função totiente de Euler, φ(n)
        # φ(n) = (p - 1) * (q - 1), onde p e q são primos
        fi = (primeiro_primo_aleatorio - 1) * (segundo_primo_aleatorio - 1)

        # Encontrar e que seja coprimo com φ(n)
        chave_publica = random.choice([i for i in range(2, fi) if math.gcd(i, fi) == 1])

        # Encontrar d tal que (d * e) % φ(n) == 1
        chave_privada = pow(chave_publica, -1, fi)

        self.chave_publica = chave_publica
        self.chave_privada = chave_privada
        self.canal = n
        return chave_publica, chave_privada, n

    # Realiza a operação de exponenciação modular de maneira eficiente
    # Calculando (base^exp) % mod
    def expo_modular(self, base, exp, mod):

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


    def codificar_msg(self, mensagem, chave_publica, canal):
        msg_codificada = []

        # Converte cada letra da mensagem em seu valor ASCII e criptografa
        for letra in mensagem:
            msg_codificada.append(self.expo_modular(ord(letra), chave_publica, canal))

        return msg_codificada

    def decodificar(self, msg_codificada, chave_privada, canal):
        msg_decodificada = ''

        # Descriptografa cada número da mensagem e converte para letra
        for num in msg_codificada:
            msg_decodificada += chr(self.expo_modular(num, chave_privada, canal))

        return msg_decodificada

    def separar_msg(self, mensagem_junta):
        return [int(p) for p in mensagem_junta.split()]