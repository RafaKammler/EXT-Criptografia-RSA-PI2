
## Criptografia RSA com Flask

### Visão Geral

Este projeto é uma aplicação web que utiliza a criptografia RSA para criptografar e descriptografar mensagens. Ele foi desenvolvido em Python, utilizando o framework Flask para criar uma API simples que lida com as operações de criptografia e descriptografia. Além disso, a aplicação permite a geração de chaves públicas e privadas que são utilizadas no processo criptográfico.

### Funcionalidades Principais

1. **Geração de chaves**: O sistema gera automaticamente um par de chaves RSA (pública e privada) para serem usadas na criptografia e descriptografia.
2. **Criptografia de mensagens**: Usando a chave pública e o "canal" (número calculado com base em dois números primos), o projeto permite criptografar uma mensagem fornecida pelo usuário.
3. **Descriptografia de mensagens**: Com a chave privada e o canal, a aplicação consegue restaurar a mensagem original que foi criptografada.
4. **Interface intuitiva**: A aplicação oferece uma interface de fácil uso, com botões que permitem gerar chaves e criptografar/descriptografar mensagens diretamente no navegador.

### Tecnologias Utilizadas

- **Python**: Linguagem principal utilizada no backend, responsável pelo processo de criptografia e a lógica de geração de chaves.
- **Flask**: Framework web para criar a API que se comunica com o frontend.
- **JavaScript (Fetch API)**: Para realizar requisições entre a interface web e o backend.
- **HTML/CSS**: Para estruturar e estilizar a interface do usuário.
- **Flask-CORS**: Para permitir o acesso da API via diferentes origens.

### Como Funciona

- Ao acessar a página, o usuário pode gerar um par de chaves clicando no botão "Gerar Chaves". Isso atualizará o DOM, exibindo as chaves pública e privada geradas.
- Com as chaves em mãos, o usuário pode criptografar uma mensagem utilizando a chave pública e o canal gerado, e posteriormente descriptografar a mensagem com a chave privada.
- O projeto utiliza conceitos de segurança como **exponenciação modular** e **totiente de Euler** para garantir a criptografia RSA de maneira eficiente.

### Como Rodar o Projeto

1. Clone o repositório e instale as dependências:
    ```bash
    pip install flask flask-cors
    ```
2. Inicie o servidor Flask:
    ```bash
    python app.py
    ```
3. Adicione os arquivos da extensão ao google por meio da ferramenta de desenvolvedor do mesmo.
