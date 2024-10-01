from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography import generate_keys, load_keys, encoder, decoder, undo_joined_message
import tempfile
import os

app = Flask(__name__)
CORS(app)

public_key_file = None
n_file = None
private_key_file = None

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
    public_key, private_key, n = load_keys()
    return jsonify({'public_key': public_key, 'private_key': private_key, 'n': n})

@app.route('/get_public_key_input', methods=['POST'])
def get_public_key_input_route():
    global public_key_file, n_file
    data = request.get_json()
    public_key = int(data['public_key'])
    n = int(data['n'])

    # Create temporary files to hold the keys
    public_key_file = create_temp_file(str(public_key))
    n_file = create_temp_file(str(n))

    return jsonify({'message': 'Public key received successfully', 'public_key': public_key, 'n': n})

# Route to receive the private key from the frontend
@app.route('/get_private_key_input', methods=['POST'])
def get_private_key_input_route():
    global private_key_file
    data = request.get_json()
    private_key = int(data['private_key'])

    # Create a temporary file to hold the private key
    private_key_file = create_temp_file(str(private_key))

    return jsonify({'message': 'Private key received successfully', 'private_key': private_key})

# Route to encrypt the message using the provided keys
@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    global public_key_file, n_file

    # Ensure the keys have been received
    if public_key_file is None or n_file is None:
        return jsonify({'error': 'Public key or N file not found'}), 400

    data = request.json
    message = data['message']

    # Read the public key and N values from the temporary files
    with open(public_key_file, 'r') as f:
        public_key = int(f.read())

    with open(n_file, 'r') as f:
        n = int(f.read())

    # Perform encryption
    message_crypto = encoder(message, public_key, n)
    encrypted_message = ' '.join(str(p) for p in message_crypto)

    return jsonify({'encrypted_text': encrypted_message})

# Route to decrypt the message using the provided private key
@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    global private_key_file, n_file

    # Ensure the keys have been received
    if private_key_file is None or n_file is None:
        return jsonify({'error': 'Private key or N file not found'}), 400

    data = request.json
    encrypted_message = data['encryptedText']

    # Read the private key and N values from the temporary files
    with open(private_key_file, 'r') as f:
        private_key = int(f.read())

    with open(n_file, 'r') as f:
        n = int(f.read())

    # Convert the encrypted message into a list of integers
    message_original = undo_joined_message(encrypted_message)

    # Perform decryption
    decrypted_message = decoder(message_original, private_key, n)

    return jsonify({'decrypted_message': decrypted_message})

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
