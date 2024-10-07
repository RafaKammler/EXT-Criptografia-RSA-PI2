from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography import gerar_chaves, codificar_msg, decodificar, separar_msg

app = Flask(__name__)
CORS(app)

# Variáveis globais para armazenar as chaves e o canal
chave_publica = None
chave_privada = None
canal = None

# Rota para gerar as chaves e retorná-las para o frontend
@app.route('/gerar_chaves', methods=['POST'])
def enviar_chaves():
    global chave_publica, chave_privada, canal
    chave_publica, chave_privada, canal = gerar_chaves()
    return jsonify({'chave_publica': chave_publica, 'chave_privada': chave_privada, 'canal': canal})

# Rota para receber a chave pública e o canal do frontend
@app.route('/rota_chave_pub', methods=['POST'])
def receber_chave_publica():
    global chave_publica, canal
    data = request.get_json()
    chave_publica = int(data['chave_publica'])
    canal = int(data['canal'])
    return jsonify({'message': 'Public key received successfully', 'public_key': chave_publica, 'n': canal})

# Rota para receber a chave privada do frontend
@app.route('/rota_chave_priv', methods=['POST'])
def receber_chave_privada():
    global chave_privada
    data = request.get_json()
    chave_privada = int(data['private_key'])
    return jsonify({'message': 'Private key received successfully', 'private_key': chave_privada})

# Rota para criptografar a mensagem usando as chaves fornecidas
@app.route('/criptografar', methods=['POST'])
def criptografar():
    conteudo = request.json
    mensagem = conteudo['mensagem']
    chave_publica = int(conteudo['chave_publica'])
    canal = int(conteudo['canal'])
    mensagem_codificada = codificar_msg(mensagem, chave_publica, canal)
    mensagem_criptografada = ' '.join(str(p) for p in mensagem_codificada)
    return jsonify({'mensagem_criptografada': mensagem_criptografada})

# Rota para descriptografar a mensagem usando a chave privada fornecida
@app.route('/descriptografar', methods=['POST'])
def descriptografar():
    conteudo = request.json
    mensagem_criptografada = conteudo['encryptedText']
    chave_privada = int(conteudo['chave_privada'])
    canal = int(conteudo['canal'])
    mensagem_criptografada_separada = separar_msg(mensagem_criptografada)
    mensagem_original = decodificar(mensagem_criptografada_separada, chave_privada, canal)
    return jsonify({'decrypted_message': mensagem_original})

if __name__ == '__main__':
    app.run(debug=True)