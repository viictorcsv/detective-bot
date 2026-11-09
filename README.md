# DetectiveBot

Jogo de investigação para Discord desenvolvido em Python. Cada jogador recebe um mistério fictício, descobre três pistas e escolhe um suspeito. Uma única acusação encerra o caso e apresenta a explicação, com acerto ou erro.

Projeto educacional para apresentação técnica do curso Python Pro da Kodland, com histórias sem violência gráfica e foco em comandos, programação assíncrona e componentes nativos do `discord.py`.

## Funcionalidades

- Três casos: **O Roubo no Museu**, **O Mistério da Biblioteca** e **O Laboratório Trancado**.
- Casos apresentados em embeds, com narrativa e três suspeitos.
- Pistas reveladas em ordem, em mensagens privadas (*ephemeral*), incluindo as anteriores para consulta.
- Botão de acusação e menu suspenso de suspeitos, utilizáveis somente pelo dono da investigação.
- Resultado privado com o culpado e a explicação lógica.
- Uma investigação ativa por jogador em cada servidor, com substituição, desistência e expiração após cinco minutos sem interação.

## Comandos

| Comando | Função |
| --- | --- |
| `/ajuda` | Mostra instruções e comandos disponíveis. |
| `/caso` | Sorteia um caso e substitui a investigação anterior, se houver. |
| `/desistir` | Encerra a investigação sem revelar a solução. |

O sorteio pode repetir um caso. Os comandos são usados em servidores; ajuda, pistas, resultado e confirmação de desistência são privados. A mensagem inicial e o menu de suspeitos aparecem no canal.

## Tecnologias e estrutura

Python **3.11 ou superior**, `discord.py` **2.x** e `python-dotenv`. Não há banco de dados, geração por IA nem integrações externas além do próprio Discord.

```text
detective-bot/
├── main.py           # Conexão, comandos, embeds, controles e estado em memória
├── casos.py          # Narrativas, suspeitos, pistas e soluções
├── requirements.txt  # Dependências
├── README.md
├── .env.example      # Modelo de configuração, sem credenciais
└── .gitignore
```

`investigacoes` associa `(ID do servidor, ID do jogador)` a uma `InvestigacaoView`. A view valida as interações e guarda o progresso. O encerramento remove esse registro e desabilita os controles. Apenas classes necessárias à interface do Discord são utilizadas.

## Configurar o Discord

1. No [Developer Portal](https://discord.com/developers/applications), crie uma aplicação chamada **DetectiveBot**.
2. Na aba **Bot**, gere o token com **Reset Token** e guarde-o para o `.env`. Os intents privilegiados podem permanecer desativados; o código utiliza apenas `guilds`.
3. Em **Installation**, habilite **Guild Install**. Nas configurações dessa instalação, selecione os escopos `bot` e `applications.commands` e as permissões **View Channels**, **Send Messages** e **Embed Links**.
4. Abra o **Install Link** e adicione o bot a um servidor de testes que você gerencie. As permissões também precisam estar liberadas no canal utilizado. Veja o [guia oficial de instalação](https://docs.discord.com/developers/quick-start/getting-started).
5. No aplicativo Discord, ative **Configurações do usuário → Avançado → Modo desenvolvedor**. Clique com o botão direito no ícone do servidor e selecione **Copiar ID do servidor**. Veja o [guia oficial de IDs](https://support.discord.com/hc/pt-br/articles/206346498).

O ID do servidor é usado em `DISCORD_GUILD_ID`. O ID do aplicativo e a chave pública não substituem esse valor nem o token. Este bot usa a conexão Gateway; não é necessário configurar um endpoint HTTP de interações.

## Instalação

Clone o projeto e entre na pasta:

```bash
git clone https://github.com/viictorcsv/detective-bot.git
cd detective-bot
python -m venv .venv
```

No **Git Bash do Windows**:

```bash
source .venv/Scripts/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

No **PowerShell**, sem precisar ativar o ambiente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

No **Linux/macOS**, crie o ambiente com `python3 -m venv .venv` e use:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Copie o modelo apenas na primeira configuração, preservando um `.env` já preenchido. Edite o `.env` na mesma pasta de `main.py`:

```dotenv
DISCORD_TOKEN=cole_seu_token_aqui
DISCORD_GUILD_ID=cole_o_id_do_servidor_aqui
```

Substitua os exemplos pelos valores reais. O `.env` é ignorado pelo Git; mantenha o `.env.example` sem credenciais. Se um token for exposto, gere outro no Developer Portal. Variáveis já definidas no ambiente têm prioridade sobre o `.env`.

## Executar e jogar

Com o ambiente ativo, no Git Bash ou Linux/macOS:

```bash
python -u main.py
```

No PowerShell:

```powershell
.\.venv\Scripts\python.exe -u main.py
```

O terminal deve informar **3 comando(s) sincronizado(s)** e **DetectiveBot online**. A sincronização acontece no login, somente no servidor indicado por `DISCORD_GUILD_ID`. Para usar outro servidor de testes, adicione o bot nele, altere esse ID e reinicie.

1. Execute `/ajuda` em um canal do servidor.
2. Execute `/caso` e leia o relato e os suspeitos.
3. Clique em **Investigar pistas** para revelar uma pista por vez. Após a terceira, o mesmo botão permite consultar todas novamente.
4. Clique em **Acusar suspeito** e escolha um nome. **A seleção é definitiva**, mesmo antes de ler todas as pistas.
5. Leia o resultado privado. Use `/caso` para jogar novamente ou `/desistir` para abandonar uma investigação ainda ativa.

Mantenha o processo aberto durante o jogo. Use `Ctrl+C` para desligar. Ao reiniciar, as investigações são perdidas e os controles das mensagens antigas deixam de funcionar; inicie outro `/caso`.

## Roteiro de testes manuais

| Cenário | Resultado esperado |
| --- | --- |
| `/ajuda` | Embed privado com os três comandos. |
| `/caso` | Relato, três suspeitos e dois botões, sem solução. |
| Revelar pistas quatro vezes | As três pistas aparecem em ordem; o quarto clique informa que não há novas evidências. |
| Acusar corretamente | Resultado verde, culpado, explicação e controles desativados. |
| Acusar incorretamente | Resultado vermelho, culpado verdadeiro, explicação e controles desativados. |
| Acusar antes de revelar pistas | A seleção também encerra o caso. |
| `/desistir` com um caso ativo | Confirmação privada, controles desativados e nenhuma solução revelada. |
| `/desistir` sem caso ou após conclusão | Mensagem informando que não existe investigação ativa. |
| `/caso` durante outra investigação | Novo caso ativo e controles anteriores desativados, inclusive um menu já aberto. |
| Outro jogador clicar nos controles | Bloqueio privado; o progresso do dono não muda. |
| Dois jogadores iniciarem casos | Investigações independentes. |
| Mesmo jogador em servidores distintos | Progresso separado; sincronize os comandos em cada servidor para testar. |
| Esperar cinco minutos sem interação | Caso encerrado e controles desativados, sem revelar a solução. |
| Apagar a mensagem e usar `/desistir` | Estado encerrado; a impossibilidade de editar é registrada no terminal. |
| Reiniciar o bot | Estado em memória limpo; use um novo `/caso`. |

Para testar acerto e erro de forma deliberada, consulte o índice `culpado` em `casos.py`: a contagem começa em zero. Para verificar a configuração, valores ausentes ou inválidos devem produzir uma mensagem de erro antes do jogo.

Verificações locais rápidas, com o ambiente ativo:

```bash
python -m py_compile main.py casos.py
python -m pip check
```

## Problemas comuns

| Problema | O que conferir |
| --- | --- |
| Token inválido | Use o token da aba **Bot**, atualizado no `.env`, e reinicie. |
| Acesso negado ao sincronizar | ID do servidor, instalação do bot e escopos `bot` e `applications.commands`. |
| Comando não aparece | Reinicie o bot atualizado, confira os três comandos sincronizados e a permissão **Use Application Commands** do jogador. |
| Falha ao enviar ou editar | Permissões no canal e existência da mensagem. O caso encerrado continua encerrado mesmo se a edição falhar. |
| Bot offline | O processo precisa estar em execução e com acesso à internet. |
| Caminho não encontrado no Git Bash | Use `python -u main.py` com a `.venv` ativa ou `./.venv/Scripts/python.exe -u main.py`. |

As histórias são fixas e as soluções estão no código-fonte. O projeto é um jogo educacional, sem persistência de partidas ou views após reinício.
