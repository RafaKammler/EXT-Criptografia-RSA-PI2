document.addEventListener('DOMContentLoaded', () => {
  const generateKeysButton = document.getElementById('generateKeys');
  const handleEncryptButton = document.getElementById('handleEncryptButton');
  const decryptButton = document.getElementById('decryptButton');
  const publicKeySpan = document.getElementById('publicKeyGenerated');
  const privateKeySpan = document.getElementById('privateKeyGenerated');
  const nSpan = document.getElementById('nGenerated');
  const nInput = document.getElementById('nInput');
  const publicKeyInput = document.getElementById('publicKeyInput');
  const privateKeyInput = document.getElementById('privateKeyInput');
  const messageInput = document.getElementById('mensageminput');
  const encryptedInput = document.getElementById('encryptedInput');
  const encryptedTextSpan = document.getElementById('encryptedText');
  const decryptedTextSpan = document.getElementById('decryptedText');

  const generateKeys = async () => {
    const response = await fetch('http://localhost:5000/generate_keys', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    publicKeySpan.textContent = data.public_key;
    privateKeySpan.textContent = data.private_key;
    nSpan.textContent = data.n;
  };

  generateKeysButton.addEventListener('click', generateKeys);

  const sendInputPublicKey = async (publicKey, message, privateKey, n) => {
    try {
      const response = await fetch('http://localhost:5000/get_public_key_input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          public_key: publicKey,
          n: n
        })
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending public key:', error);
    }
  };

  const sendInputPrivateKey = async (privateKey, n) => {
    try {
      const response = await fetch('http://localhost:5000/get_private_key_input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ private_key: privateKey, n: n })
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending private key:', error);
    }
  };

  const encryptMessage = async (message) => {
    try {
      const response = await fetch('http://localhost:5000/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      const data = await response.json();
      encryptedTextSpan.textContent = data.encrypted_text;
    } catch (error) {
      console.error('Error encrypting message:', error);
    }
  };

  const decryptMessage = async (encryptedText) => {
    try {
      const response = await fetch('http://localhost:5000/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ encryptedText })
      });
      const data = await response.json();
      decryptedTextSpan.textContent = data.decrypted_message;
    } catch (error) {
      console.error('Error decrypting message:', error);
    }
  };

  const handleEncryptClick = async () => {
    const publicKey = publicKeyInput.value;
    const message = messageInput.value;
    const n = nInput.value;
    await sendInputPublicKey(publicKey, message, null, n);
    await encryptMessage(message);
  };

  const handleDecryptClick = async () => {
    const privateKey = privateKeyInput.value;
    const encryptedText = encryptedInput.value;
    const n = nInput.value;
    await sendInputPrivateKey(privateKey, n);
    await decryptMessage(encryptedText);
  };

  handleEncryptButton.addEventListener('click', handleEncryptClick);
  decryptButton.addEventListener('click', handleDecryptClick);
});