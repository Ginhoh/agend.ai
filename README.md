# ConsultaDB

Servidor MCP para operações de cadastro e agenda de uma barbearia, com persistência local em SQLite. O projeto demonstra como disponibilizar operações de domínio como ferramentas que um cliente compatível com o Model Context Protocol (MCP) pode descobrir e invocar.

## Visão geral

O servidor, implementado com `FastMCP`, registra ferramentas para consultar e manter clientes, barbeiros, serviços, horários de trabalho e agendamentos. Os dados são armazenados no arquivo `db.db`; não há API HTTP, interface gráfica ou camada de ORM neste projeto.

O fluxo de uso é:

1. Inicializar o esquema SQLite.
2. Iniciar `server.py` como processo MCP via stdio.
3. Conectar um cliente MCP ao processo e usar as ferramentas registradas.

## Funcionalidades

- **Clientes:** cadastrar, listar, buscar por ID, nome ou e-mail, alterar dados e remover.
- **Barbeiros:** cadastrar, listar, buscar por ID ou nome, alterar nome, ativar/desativar e remover.
- **Serviços:** cadastrar, listar, buscar por ID ou nome, alterar preço ou duração e remover.
- **Horários de trabalho:** cadastrar, listar, alterar início ou término e remover horários por barbeiro e dia da semana.
- **Agendamentos:** criar, consultar por ID, listar por cliente, barbeiro ou dia, reagendar, cancelar, concluir e marcar ausência.
- **Disponibilidade:** consultar horários disponíveis de um barbeiro em uma data, informada no formato `DD/MM/YYYY`.

## Tecnologias

- Python 3.12 ou superior.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), usando `mcp.server.fastmcp`.
- SQLite, pela biblioteca padrão `sqlite3`.

O repositório não contém atualmente um `requirements.txt` ou outro manifesto de dependências. O SDK MCP é a dependência externa identificada no código.

## Estrutura

```text
.
├── database.py              # Criação das tabelas SQLite e experimento local
├── server.py                # Inicialização do servidor MCP e registro das ferramentas
├── db.db                    # Banco SQLite local
├── tables_tb.txt            # Anotações/rascunho do modelo de dados
└── tools/
    ├── agendamentos.py      # Operações de agenda e disponibilidade
    ├── barbeiros.py         # Operações de barbeiros
    ├── clientes.py          # Operações de clientes
    ├── horarios_trabalho.py # Operações de horários
    └── servicos.py          # Operações de serviços
```

`tempCodeRunnerFile.py` e `tools/tempCodeRunnerFile.py` são arquivos auxiliares de experimentação, não utilizados pelo servidor.

## Instalação e execução

No PowerShell, a partir da raiz do projeto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install mcp
```

Inicialize o banco sem executar o experimento presente no bloco principal de `database.py`:

```powershell
python -c "import database"
```

Esse comando cria as tabelas em `db.db` no diretório de trabalho atual. Em seguida, inicie o servidor:

```powershell
python server.py
```

O servidor usa o transporte stdio do MCP. Portanto, normalmente ele deve ser iniciado pelo cliente MCP, e não mantido em um terminal interativo separado. O diretório de trabalho precisa ser a raiz do projeto, pois as ferramentas abrem `db.db` por caminho relativo.

### Configuração no VS Code

Para um workspace aberto na raiz deste repositório, uma configuração de exemplo em `.vscode/mcp.json` é:

```json
{
  "servers": {
    "consulta-db": {
      "type": "stdio",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": ["${workspaceFolder}\\server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

Crie/inicialize `db.db` antes de conectar o cliente. Para outros clientes MCP, configure um servidor stdio equivalente apontando para o interpretador do ambiente virtual e para `server.py`, com a raiz do projeto como diretório de trabalho.

## Modelo de dados

O esquema criado por `database.py` contém:

| Tabela | Campos principais |
| --- | --- |
| `clientes` | `id`, `nome`, `email`, `telefone`, `data_nascimento`, `ativo` |
| `barbeiros` | `id`, `nome`, `ativo` |
| `servicos` | `id`, `nome`, `duracao_minutos`, `preco` |
| `horarios_trabalho` | `id`, `barbeiro_id`, `dia_semana`, `hora_inicio`, `hora_fim` |
| `agendamentos` | `id`, `id_cliente`, `barbeiro_id`, `servico`, `data_hora_inicio`, `data_hora_fim`, `status` |
| `bloqueios` | `id`, `barbeiro_id`, `data_hora_inicio`, `data_hora_fim` |

Datas e horários são armazenados como texto. Os campos de relação com barbeiros, clientes e serviços estão declarados como colunas, mas o esquema atual não cria restrições de chave estrangeira efetivas. A tabela `bloqueios` é criada, porém ainda não possui ferramentas MCP para consulta ou manutenção.

## Formatos esperados

- Data: `DD/MM/YYYY` (por exemplo, `08/09/2026`).
- Data e hora de agendamento: `DD/MM/YYYY HH:MM`.
- Dia da semana: nome em português sem acentos, como `segunda`, `terca` ou `sabado`.
- Horários de trabalho: `HH:MM`.

## Limitações conhecidas

- A disponibilidade ainda tem regras experimentais: utiliza a duração do serviço de ID `1` e não considera corretamente todos os casos de conflito ou status de agendamento.
- `database.py` contém lógica de teste no bloco `__main__` que pressupõe cadastros existentes; por isso, o comando de inicialização acima importa o módulo em vez de executá-lo diretamente.
- Algumas consultas interpolam valores recebidos diretamente no SQL, e algumas ferramentas não tratam corretamente resultados múltiplos ou a ausência de registros. Validação de entrada, parâmetros SQL consistentes e testes automatizados são próximos passos importantes.
- O caminho do banco é relativo ao diretório de trabalho; executar o servidor fora da raiz pode criar ou acessar outro arquivo `db.db`.
- Não há suíte de testes automatizados nem arquivo de dependências versionado no momento.

## Possíveis evoluções

- Adicionar testes para operações CRUD, transições de status e conflitos de agenda.
- Modelar chaves estrangeiras e índices, habilitando integridade referencial no SQLite.
- Validar datas, horários, duração, disponibilidade e transições permitidas antes de gravar.
- Parametrizar todas as consultas e padronizar respostas de erro e resultados de listagem.
- Separar a inicialização do esquema dos experimentos locais e versionar as dependências.