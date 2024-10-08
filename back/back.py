from flask import Flask, request, jsonify
from flask_cors import CORS
from criptografia import CriptografiaRSA

app = Flask(__name__)
CORS(app)

# Inicia a classe para o servidor
class Servidor(CriptografiaRSA):
    def __init__(self):
        super().__init__()
        self.chave_publica = None
        self.chave_privada = None
        self.canal = None

        # Adiciona as rotas para o servidor
        app.add_url_rule('/gerar_chaves', 'enviar_chaves', self.enviar_chaves, methods=['POST'])
        app.add_url_rule('/criptografar', 'criptografar', self.criptografar, methods=['POST'])
        app.add_url_rule('/descriptografar', 'descriptografar', self.descriptografar, methods=['POST'])


    # Função para enviar as chaves públicas e privadas para o JS
    def enviar_chaves(self):
        self.gerar_chaves()
        return jsonify({'chave_publica': self.chave_publica, 'chave_privada': self.chave_privada, 'canal': self.canal})


    # Função para criptografar a mensagem
    def criptografar(self):

        # Recebe a mensagem e a chave pública
        conteudo = request.json
        mensagem_normal = conteudo['mensagem']
        self.chave_publica = int(conteudo['chave_publica'])
        self.canal = int(conteudo['canal'])

        # Codifica a mensagem e a transforma em uma string
        mensagem_cripto = self.codificar_msg(mensagem_normal, self.chave_publica, self.canal)
        mensagem_criptografada = ' '.join(str(p) for p in mensagem_cripto)

        return jsonify({'mensagem_criptografada': mensagem_criptografada})


    # Função para descriptografar a mensagem
    def descriptografar(self):

        # Recebe a mensagem criptografada e a chave privada
        conteudo = request.json
        mensagem_criptografada = conteudo['encryptedText']
        self.chave_privada = int(conteudo['chave_privada'])
        self.canal = int(conteudo['canal'])

        # Separa a mensagem criptografada e a descriptografa
        mensagem_criptografada_separada = self.separar_msg(mensagem_criptografada)
        mensagem_original = self.decodificar(mensagem_criptografada_separada, self.chave_privada, self.canal)

        return jsonify({'decrypted_message': mensagem_original})


# Inicia o servidor
if __name__ == '__main__':
    servidor = Servidor()
    app.run(debug=True)