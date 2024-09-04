# WhatsApp Bot

Este projeto é um bot para WhatsApp que utiliza o Selenium para automatizar conversas. O bot coleta informações dos usuários, permite revisar e confirmar as informações coletadas e termina a conversa após um período de inatividade ou por decisão do usuário.

## Funcionalidades

- **Coleta de Informações:** O bot faz uma série de perguntas ao usuário e coleta suas respostas.
- **Revisão de Informações:** Após coletar todas as informações, o bot exibe um resumo para o usuário confirmar ou corrigir.
- **Encerramento da Conversa:** Se o usuário não responder dentro de 30 segundos, a conversa é encerrada automaticamente.
- **Mensagens Dinâmicas:** As perguntas podem ser facilmente editadas no código.

## Pré-requisitos

- Python 3.x
- Selenium
- WebDriver do Chrome (ChromeDriver)

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/whatsapp-bot.git
   cd whatsapp-bot
   ```

2. **Instale as dependências:**

   ```bash
   pip install selenium
   ```

3. **Baixe e coloque o `chromedriver` na pasta do projeto:**
   - Baixe o ChromeDriver compatível com sua versão do Chrome a partir de [aqui](https://sites.google.com/a/chromium.org/chromedriver/downloads).
   - Coloque o `chromedriver` na pasta do projeto ou adicione-o ao PATH do sistema.

## Configuração

1. **Atualize o arquivo `bot.py`:**

   - O bot utiliza o perfil do navegador armazenado em `profile/zap`. Certifique-se de que o perfil esteja configurado corretamente para o WhatsApp Web.
   - Edite as perguntas no código conforme necessário, alterando a variável `perguntas`.

2. **Configure o WebDriver:**
   - Certifique-se de que o caminho para o `chromedriver` está correto e o arquivo `chromedriver` tem permissões de execução.

## Uso

1. **Execute o script do bot:**

   ```bash
   python bot.py
   ```

2. **Interaja com o bot:**
   - O bot irá procurar novas notificações no WhatsApp Web.
   - Após encontrar uma mensagem, ele começará a coletar informações conforme definido nas perguntas.
   - Se necessário, o bot permitirá revisar e confirmar as informações coletadas.

## Exemplo de Execução

```plaintext
Nova notificação encontrada.
Mensagem recebida: Olá!
Mensagem recebida: Sim.
Mensagem recebida: João Silva.
Mensagem recebida: 123456
Mensagem recebida: Detalhes adicionais.
As informações estão corretas? Responda 'sim' para confirmar ou 'não' para refazer algo.
Informações revisadas e confirmadas: ['João Silva', '123456', 'Detalhes adicionais.']
```
