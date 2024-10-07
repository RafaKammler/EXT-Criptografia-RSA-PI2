from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography import CriptografiaRSA

app = Flask(__name__)
CORS(app)

class Servidor(CriptografiaRSA):
    def __init__(self):
        super().__init__()
        self.chave_publica = None
        self.chave_privada = None
        self.canal = None


        app.add_url_rule('/gerar_chaves', 'enviar_chaves', self.enviar_chaves, methods=['POST'])
        app.add_url_rule('/criptografar', 'criptografar', self.criptografar, methods=['POST'])
        app.add_url_rule('/descriptografar', 'descriptografar', self.descriptografar, methods=['POST'])

    def enviar_chaves(self):
        self.gerar_chaves()
        return jsonify({'chave_publica': self.chave_publica, 'chave_privada': self.chave_privada, 'canal': self.canal})

    def criptografar(self):
        conteudo = request.json
        mensagem_normal = conteudo['mensagem']
        self.chave_publica = int(conteudo['chave_publica'])
        self.canal = int(conteudo['canal'])
        mensagem_cripto = self.codificar_msg(mensagem_normal, self.chave_publica, self.canal)
        mensagem_criptografada = ' '.join(str(p) for p in mensagem_cripto)
        return jsonify({'mensagem_criptografada': mensagem_criptografada})

    def descriptografar(self):
        conteudo = request.json
        mensagem_criptografada = conteudo['encryptedText']
        self.chave_privada = int(conteudo['chave_privada'])
        self.canal = int(conteudo['canal'])
        mensagem_criptografada_separada = self.separar_msg(mensagem_criptografada)
        mensagem_original = self.decodificar(mensagem_criptografada_separada, self.chave_privada, self.canal)
        return jsonify({'decrypted_message': mensagem_original})

if __name__ == '__main__':
    servidor = Servidor()
    app.run(debug=True)