## Jogo multiplayer utilizando Sockets

Projeto desenvolvido na disciplina de Programação Concorrente, Paralela e Distribuída com o objetivo de implementar um jogo multiplayer utilizando comunicação via sockets.

O jogo escolhido chama-se Gomoku. O jogador deve tentar fazer uma sequência ininterrupta de 5 peças na horizontal, vertical ou diagonal, em um tabuleiro 15x15.

### Como inicializar o jogo

#### Iniciando o servidor

Primeiro, deve-se inicializar o servidor contido no arquivo server.py:

```
python3 .\server.py
```

Como padrão ele é inicializado sempre na porta 5000.

#### Iniciando os clientes

Cada jogador possui seu próprio cliente. O primeiro cliente a conectar no servidor será o jogador 1 e ele aguardará a conexão do segundo cliente.

```
python3 .\client.py 127.0.0.1 5000
```
