document.addEventListener('DOMContentLoaded', () => {
  // Seleciona os elementos do DOM
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
  const copyEncryptedTextButton = document.getElementById('copyEncryptedText');
  const copyDecryptedTextButton = document.getElementById('copyDecryptedText');

  // Função para fazer requisições à API
  const conexaoAPI = async (url, method, body = null) => {
    const config = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) config.body = JSON.stringify(body);
    const response = await fetch(url, config);
    return response.json();
  };

  // Função para gerar chaves e atualizar o DOM
  const gerarChaves = async () => {
    const data = await conexaoAPI('http://localhost:5000/gerar_chaves', 'POST');
    chavePublicaSpan.textContent = data.chave_publica;
    chavePrivadaSpan.textContent = data.chave_privada;
    canalSpan.textContent = data.canal;
  };

  // Função para criptografar a mensagem e atualizar o DOM
  const criptografarMensagem = async () => {
    const mensagem = inputMensagem.value;
    const chavePublica = chavePublicaInput.value;
    const canal = canalInput.value;
    const data = await conexaoAPI('http://localhost:5000/criptografar', 'POST', { mensagem, chave_publica: chavePublica, canal });
    textoCriptografadoSpan.textContent = data.mensagem_criptografada;
  };

  // Função para descriptografar a mensagem e atualizar o DOM
  const descriptografarMensagem = async () => {
    const textoCriptografado = inputMensagemCriptografada.value;
    const chavePrivada = chavePrivadaInput.value;
    const canal = canalInput.value;
    const data = await conexaoAPI('http://localhost:5000/descriptografar', 'POST', { encryptedText: textoCriptografado, chave_privada: chavePrivada, canal });
    textoDescriptografadoSpan.textContent = data.decrypted_message;
  };

  const copyToClipboard = (element) => {
    element.select();
    document.execCommand('copy');
  };

  // Adiciona eventos de clique aos botões
  botaoGerarChaves.addEventListener('click', gerarChaves);
  botaoCriptografar.addEventListener('click', criptografarMensagem);
  botaoDescriptografar.addEventListener('click', descriptografarMensagem);
  copyEncryptedTextButton.addEventListener('click', () => copyToClipboard(textoCriptografadoSpan));
  copyDecryptedTextButton.addEventListener('click', () => copyToClipboard(textoDescriptografadoSpan));
});