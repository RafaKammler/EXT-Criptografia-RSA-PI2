document.addEventListener('DOMContentLoaded', () => {
  const generateKeysButton = document.getElementById('generateKeys');
  const publicKeySpan = document.getElementById('publicKeyGenerated');
  const privateKeySpan = document.getElementById('privateKeyGenerated');
  const searchKeysButton = document.getElementById('searchKeysButton')
  const channelSpan = document.getElementById('channelSpan')

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
  };


  generateKeysButton.addEventListener('click', generateKeys);

  function searchText() {
    try {
      const pageText = document.body.innerText;
      const match = pageText.includes('canal: ')
      if (match) {

        canalIndex = pageText.indexOf('canal: ');
        textAfterCanal = pageText.substring(canalIndex + 'canal: '.length).trim();
        canal = textAfterCanal[0];
        connectionChannel = canal;
        return connectionChannel;
      }
    }
    catch (error) {
      console.log("erro")
    }
  }
  const searchKeys = async () => {
    try{
    connectionChannel = searchText();
    const response = await fetch('http://localhost:5000/get_channel',
      {
        method: 'POST',
        headers:
        {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ channel: connectionChannel })
      }

    );
    channelSpan.textContent = connectionChannel;
  } catch(err){
  }
  
  }
  searchKeysButton.addEventListener('click', searchKeys)

  const sendInputPublicKey = async (publicKey) => {
    try {
      const response = await fetch('http://localhost:5000/get_public_key_input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ public_key: publicKey })
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending public key:', error);
    }
  };

  const sendInputPrivateKey = async (privateKey) => {
    try {
      const response = await fetch('http://localhost:5000/get_private_key_input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ private_key: privateKey })
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending private key:', error);
    }
  };

  const encryptMessage = async () => {
    try {
      const response = await fetch('http://localhost:5000/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      const data = await response.json();
      setEncryptedText(data.encrypted_text);
    } catch (error) {
      console.error('Error encrypting message:', error);
    }
  };

  const decryptMessage = async () => {
    try {
      const response = await fetch('http://localhost:5000/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ encryptedText })
      });
      const data = await response.json();
      setDecryptedText(data.decrypted_message);
    } catch (error) {
      console.error('Error decrypting message:', error);
    }
  };

  const handleEncryptClick = async () => {
    await sendInputPublicKey(publicKeyInput);
    await encryptMessage();
  };

  const handleDecryptClick = async () => {
    await sendInputPrivateKey(privateKeyInput);
    await decryptMessage();
  };
});