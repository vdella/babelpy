# Discord bot para reportar dias restantes de estoque

Este exemplo mostra uma estrutura simples para um bot Discord que:

1. lê dados de planilhas (Google Sheets ou Excel local),
2. calcula dias restantes por SKU (`estoque / média diária`),
3. envia resultado sob comando (`/dias_estoque`) e em rotina diária.

## Estrutura

- `bot.py`: inicializa o bot e registra comandos/rotinas.
- `config.py`: valida variáveis de ambiente.
- `data_sources.py`: leitura de dados (Google Sheets e Excel).
- `stock_days.py`: regras de cálculo e formatação de saída.
- `requirements.txt`: dependências.
- `.env.example`: exemplo de configuração.

## Como usar (resumo)

1. Crie um app no Discord Developer Portal e pegue o token.
2. Copie `.env.example` para `.env` e preencha os campos.
3. Escolha uma fonte:
   - `DATA_SOURCE=google_sheets` para Google Sheets; ou
   - `DATA_SOURCE=excel` para arquivo `.xlsx` local.
4. Instale dependências e execute:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python bot.py
```

## Regras aplicadas no cálculo de dias

- Se `media_diaria <= 0`, dias restantes = `0`.
- Se valores inválidos (vazio, texto, erro), dias restantes = `0`.
- Resultado é arredondado para cima (`ceil`).
