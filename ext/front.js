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

  const conexaoAPI = async (url, method, body = null) => {
    const config = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) config.body = JSON.stringify(body);
    const response = await fetch(url, config);
    return response.json();
  };

  const gerarChaves = async () => {
    const data = await conexaoAPI('http://localhost:5000/gerar_chaves', 'POST');
    chavePublicaSpan.textContent = data.chave_publica;
    chavePrivadaSpan.textContent = data.chave_privada;
    canalSpan.textContent = data.canal;
  };

  const criptografarMensagem = async () => {
    const mensagem = inputMensagem.value;
    const chavePublica = chavePublicaInput.value;
    const canal = canalInput.value;
    const data = await conexaoAPI('http://localhost:5000/criptografar', 'POST', { mensagem, chave_publica: chavePublica, canal });
    textoCriptografadoSpan.textContent = data.mensagem_criptografada;
  };

  const descriptografarMensagem = async () => {
    const textoCriptografado = inputMensagemCriptografada.value;
    const chavePrivada = chavePrivadaInput.value;
    const canal = canalInput.value;
    const data = await conexaoAPI('http://localhost:5000/descriptografar', 'POST', { encryptedText: textoCriptografado, chave_privada: chavePrivada, canal });
    textoDescriptografadoSpan.textContent = data.decrypted_message;
  };

  botaoGerarChaves.addEventListener('click', gerarChaves);
  botaoCriptografar.addEventListener('click', criptografarMensagem);
  botaoDescriptografar.addEventListener('click', descriptografarMensagem);
});