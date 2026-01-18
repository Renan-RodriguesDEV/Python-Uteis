# Python Úteis

Coleção de utilitários, bibliotecas e ferramentas úteis em Python para diversos propósitos, incluindo automação, APIs, conexões com bancos de dados, processamento de dados e muito mais.

## 📋 Descrição

Este repositório contém uma variedade de scripts e módulos Python organizados por funcionalidade, projetados para facilitar tarefas comuns de desenvolvimento, automação e integração com serviços externos.

## 🗂️ Estrutura do Projeto

```
src/
├── apis/                    # Integrações com APIs externas
│   ├── whatsapp/           # Integração WhatsApp (Twilio e Meta)
│   └── tests/              # Testes de APIs (TikTok, Google Sheets)
├── connections/             # Conexões com bancos de dados
├── emails/                  # Envio e leitura de emails
├── gerador_contratos/       # Gerador de contratos em DOCX
├── imagens/                 # Processamento de imagens
├── imports_relativos/       # Exemplos de imports relativos
├── loggers/                 # Sistema de logging colorido
├── messageria/              # Sistema de mensageria
├── mylibs/                  # Bibliotecas personalizadas
├── poo_with_python/         # Exemplos de POO
├── test/                    # Testes diversos
├── tratamentos_pdf/         # Leitura e manipulação de PDFs
└── web_automacao/           # Automação web com Selenium e Playwright
```

## 🚀 Funcionalidades Principais

### 🔌 Conexões com Banco de Dados
- **MySQL Connector**: Classes para gerenciar conexões MySQL
- **SQLAlchemy ORM**: Integração com ORM para banco de dados
- **PyMySQL**: Conexões alternativas com MySQL

### 📧 Gerenciamento de Emails
- **SMTP Sender**: Envio de emails via SMTP (Gmail)
- **SendGrid**: Integração com SendGrid para envio de emails
- **Email Reader**: Leitura de emails usando IMAP

### 🤖 Automação Web
- **Selenium**: Automação de navegadores (Chrome, Edge)
- **Playwright**: Automação moderna de navegadores
- Scripts para scraping e testes automatizados

### 📱 Integrações de APIs
- **WhatsApp (Twilio)**: Envio de mensagens via Twilio
- **WhatsApp (Meta)**: Integração com Meta API
- **TikTok Scraper**: Coleta de dados do TikTok
- **Google Sheets**: Integração com planilhas Google

### 📄 Processamento de Documentos
- **Gerador de Contratos**: Aplicação Flask para gerar contratos DOCX
- **PDF Reader**: Leitura e extração de texto de PDFs com PyPDF2
- **OCR**: Processamento de imagens com Tesseract

### 🔍 Bibliotecas Customizadas
- **TikTok Scraper**: Scraping de perfis do TikTok com Playwright
- **VJ Classifier**: Classificador com PyTorch e Ultralytics
- **Data Saver**: Utilitários para salvar dados de sessão

### 📊 Sistema de Logging
- Logger colorido com suporte a rotação de arquivos
- Formatação customizada com timestamps
- Níveis de log com cores diferenciadas (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

### Dependências Principais

O projeto utiliza as seguintes bibliotecas:

- **Web & Automação**: selenium, playwright, requests
- **Banco de Dados**: mysql-connector, PyMySQL, SQLAlchemy
- **APIs & Mensagens**: twilio, sendgrid, google-api-python-client
- **Processamento**: PyPDF2, Pillow, opencv-python, pytesseract
- **Machine Learning**: torch, torchvision, ultralytics, numpy
- **Web Framework**: fastapi, uvicorn, flask
- **Utilitários**: python-dotenv, colorama, imap-tools

## 💻 Uso

### Exemplo: Conexão com MySQL

```python
from src.connections.classql import ClassConnection

# Criar conexão
conn = ClassConnection(
    host="localhost",
    user="root",
    database="meu_banco",
    password="senha",
    port=3306
)

# Conectar
connection = conn.connected()
cursor = conn.get_cursor()

# Executar query
cursor.execute("SELECT * FROM tabela")
resultados = cursor.fetchall()

# Fechar conexão
conn.desconected()
```

### Exemplo: Envio de Email via SMTP

```python
from src.emails.mailSenderSMTP import createEmailMsg

createEmailMsg(
    from_msg="seu_email@gmail.com",
    to_msg="destinatario@email.com",
    password="sua_senha",
    body="<p>Corpo do email em HTML</p>",
    attachment_path="caminho/para/arquivo.pdf"
)
```

### Exemplo: Automação Web com Selenium

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

service = webdriver.ChromeService()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.exemplo.com")
elemento = driver.find_element(By.ID, "search")
elemento.send_keys("Python")

driver.quit()
```

### Exemplo: Logger Colorido

```python
from src.loggers.logger import logger

logger.debug("Mensagem de debug")
logger.info("Mensagem informativa")
logger.warning("Aviso")
logger.error("Erro")
logger.critical("Erro crítico")
```

### Exemplo: Gerador de Contratos

Execute a aplicação Flask:

```bash
cd src/gerador_contratos
python app.py
```

Acesse: `http://localhost:5000`

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na pasta `src/configs/` com as seguintes variáveis:

```env
# Twilio WhatsApp
account_sid=seu_account_sid
auth_token=seu_auth_token
my_number=seu_numero

# Email
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_senha

# Banco de Dados
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=senha
DB_NAME=nome_banco
```

## 📋 Requisitos do Sistema

### Para Web Scraping e Automação
- **Playwright**: Requer instalação de navegadores
  ```bash
  playwright install
  ```
- **Selenium**: WebDriver Manager já incluído nas dependências
- **Tesseract OCR**: Necessário para OCR (instalação separada)
  - Windows: [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`

## 🧪 Testes

Execute os testes disponíveis:

```bash
python -m pytest src/test/
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

## 📝 Notas

- **Segurança**: Nunca commite arquivos `.env` ou credenciais sensíveis
- **Paths**: Alguns scripts contêm caminhos absolutos que precisam ser ajustados para seu ambiente
- **Configurações**: Revise as configurações antes de executar scripts de produção

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional e desenvolvimento.

## 👤 Autor

**Renan Rodrigues**
- GitHub: [@Renan-RodriguesDEV](https://github.com/Renan-RodriguesDEV)

## 🙏 Agradecimentos

Agradecimentos a todos que contribuíram com ideias e código para este projeto!

---

**Desenvolvido com ❤️ em Python**
