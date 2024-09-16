from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography import generate_keys, load_keys, encoder, decoder, undo_joined_message
import tempfile
import os

app = Flask(__name__)
CORS(app)

# Função para criar e garantir que os arquivos temporários sejam removidos
def create_temp_file(content):
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt')
    temp_file.write(content)
    temp_file.close()
    return temp_file.name

# Roteamento para gerar chaves
@app.route('/generate_keys', methods=['POST'])
def generate_keys_route():
    generate_keys()
    public_key, private_key, _ = load_keys()
    return jsonify({'public_key': public_key, 'private_key': private_key})

# Roteamento para armazenar a chave pública temporariamente
@app.route('/get_public_key_input', methods=['POST'])
def get_public_key_input_route():
    data = request.get_json()
    public_key = int(data.get('public_key'))
    
    public_key_file = create_temp_file(str(public_key))

    return jsonify({'message': 'Public key received successfully', 'public_key': public_key, 'file_path': public_key_file})

# Roteamento para armazenar a chave privada temporariamente
@app.route('/get_private_key_input', methods=['POST'])
def get_private_key_input_route():
    data = request.get_json()
    private_key = int(data.get('private_key'))
    
    private_key_file = create_temp_file(str(private_key))

    return jsonify({'message': 'Private key received successfully', 'private_key': private_key, 'file_path': private_key_file})


@app.route('/get_channel', methods=['POST'])
def receive_channel():
    global n
    data = request.get_json()
    n = data['channel']
# Roteamento para criptografar a mensagem
@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    data = request.json
    message = data['message']
    

    _, _, n = load_keys()
    public_key_file = create_temp_file(str(load_keys()[0]))

    with open(public_key_file, 'r') as f:
        public_key = int(f.read())

    message_crypto = encoder(message, public_key, n)
    encrypted_message = ' '.join(str(p) for p in message_crypto)

    os.remove(public_key_file) 

    return jsonify({'encrypted_text': encrypted_message})

# Roteamento para descriptografar a mensagem
@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    data = request.json
    encrypted_message = data['encryptedText']

    # Gerar chaves temporárias e ler o valor de N
    _, _, n = load_keys()
    private_key_file = create_temp_file(str(load_keys()[1]))

    with open(private_key_file, 'r') as f:
        private_key = int(f.read())

    message_original = undo_joined_message(encrypted_message)
    decrypted_message = decoder(message_original, private_key, n)

    os.remove(private_key_file)  # Remove o arquivo temporário após o uso

    return jsonify({'decrypted_message': decrypted_message})

if __name__ == '__main__':
    app.run(debug=True)
