document.addEventListener('DOMContentLoaded', () => {
  const botaoGerarChaves = document.getElementById('gerarChaves');
  const botaoCriptografar = document.getElementById('botaoCriptografar');
  const botaoDescriptografar = document.getElementById('botaoDescriptografar');
  const chavePublicaSpan = document.getElementById('chavePublicaGerada');
  const chavePrivadaSpan = document.getElementById('chavePrivadaGerada');
  const canalSpan = document.getElementById('canalGerado');
  const canalInput = document.getElementById('canalInput');
  const chavePublicaInput = document.getElementById('chavePublicaInput');
  const chavePrivadaInput = document.getElementById('chavePrivadaInput');
  const inputMensagem = document.getElementById('mensagemInput');
  const inputMensagemCriptografada = document.getElementById('textoCriptografado');
  const textoCriptografadoSpan = document.getElementById('encryptedText');
  const textoDescriptografadoSpan = document.getElementById('textoDescriptografado');

  const gerarChaves = async () => {
    const response = await fetch('http://localhost:5000/gerar_chaves', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    chavePublicaSpan.textContent = data.chave_publica;
    chavePrivadaSpan.textContent = data.chave_privada;
    canalSpan.textContent = data.canal;
  };

  botaoGerarChaves.addEventListener('click', gerarChaves);

  const sendInputPublicKey = async (chavePublica, n) => {
    try {
      const response = await fetch('http://localhost:5000/rota_chave_pub', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          chave_publica: chavePublica,
          canal: n,
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
      const response = await fetch('http://localhost:5000/rota_chave_priv', {
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

  const encryptMessage = async (mensagem, chavePublica, canal) => {
    try {
      const response = await fetch('http://localhost:5000/criptografar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagem, chave_publica: chavePublica, canal })
      });
      const data = await response.json();
      textoCriptografadoSpan.textContent = data.mensagem_criptografada;
    } catch (error) {
      console.error('Error encrypting message:', error);
    }
  };

  const decryptMessage = async (textoCriptografado, chavePrivada, canal) => {
    try {
      const response = await fetch('http://localhost:5000/descriptografar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ encryptedText: textoCriptografado, chave_privada: chavePrivada, canal })
      });
      const data = await response.json();
      textoDescriptografadoSpan.textContent = data.decrypted_message;
    } catch (error) {
      console.error('Error decrypting message:', error);
    }
  };

  const handleEncryptClick = async () => {
    const chavePublica = chavePublicaInput.value;
    const message = inputMensagem.value;
    const n = canalInput.value;
    await sendInputPublicKey(chavePublica, n);
    await encryptMessage(message, chavePublica, n);
  };

  const handleDecryptClick = async () => {
    const privateKey = chavePrivadaInput.value;
    const textoCriptografado = inputMensagemCriptografada.value;
    const n = canalInput.value;
    await sendInputPrivateKey(privateKey, n);
    await decryptMessage(textoCriptografado, privateKey, n);
  };

  botaoCriptografar.addEventListener('click', handleEncryptClick);
  botaoDescriptografar.addEventListener('click', handleDecryptClick);
});