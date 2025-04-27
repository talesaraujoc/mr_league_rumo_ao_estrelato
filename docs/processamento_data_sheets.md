# 📄 Documentação: Processamento do DataFrame

Este documento descreve as etapas de tratamento dos dados extraídos da planilha `season_2025` no projeto `MR_LEAGUE_RUMO_AO_ESTRELATO`.

## 🎯 Objetivo

- Transformar os dados brutos da planilha em um `DataFrame` tratado.
- Calcular uma coluna adicional chamada `PTS` (Pontuação).
- Garantir que os dados estejam limpos e no formato adequado para visualizações no Dash.

---

## 🛠️ Etapas do Processamento

### 1. Carregamento dos Dados

- Os dados são extraídos da aba `main` da planilha `season_2025` no Google Sheets.
- A conexão é realizada através de uma **Service Account** autenticada.

### 2. Limpeza Inicial

- Todos os dados inicialmente são carregados como `string` (`dtype=str`).

### 3. Conversão de Tipos

- As seguintes colunas são convertidas para o tipo `int`:
  - `V`, `E`, `D`, `GOL`, `ASS`, `STG`, `GC`, `AMA`, `AZUL`, `VER`, `PP`, `GS`, `DD`, `DP`, `FALTA`
- Valores ausentes ou inválidos são preenchidos com `0` antes da conversão.

### 4. Cálculo da Coluna `PTS`

- A coluna `PTS` representa a **pontuação individual** de cada jogador.
- O cálculo é baseado nos critérios específicos para cada `POSIÇÃO`:

| Posição | Critérios (V, E, D, GOL, ASS, STG, GC, AMA, AZUL, VER, PP, GS, DD, DP) |
|:--------|:----------------------------------------------------------------------|
| ATA     | 7, 0, -4, 7, 4, 2, -10, -4, -8, -16, -10, 0, 0, 0 |
| MEI     | 7, 0, -4, 8.5, 5, 2.5, -10, -4, -8, -16, -10, 0, 0, 0 |
| ZAG     | 7, 0, -4, 10, 6, 3, -10, -4, -8, -16, -10, 0, 0, 0 |
| GK      | 6, 0, -3, 16, 10, 4, -10, -4, -8, -16, -10, -5, 5, 20 |

- Para cada linha:
  - Multiplicamos a quantidade de eventos (gols, assistências, etc) pelos respectivos pesos definidos por posição.
  - A soma final determina o valor de `PTS`.

### 5. Tratamento de DataFrame vazio

- Caso a competição filtrada não contenha dados (ex: COPA ainda sem jogos), o sistema:
  - Exibe "Sem dados" para o primeiro colocado.
  - Evita erros no carregamento dos gráficos.

---

## 📈 Resultado Final

O `DataFrame` tratado possui as seguintes características:

- Colunas principais numéricas corrigidas.
- Nova coluna `PTS` calculada corretamente.
- Pronto para alimentar os componentes visuais do Dashboard.

---

## 🧩 Estrutura resumida do DataFrame final

| Coluna | Tipo | Descrição |
|:-------|:-----|:----------|
| DATA | str | Data da partida |
| COMPETIÇÃO | str | Tipo de competição (LIGA, COPA) |
| RODADA | int | Número da rodada |
| PARTIDA | int | Número da partida |
| PLAYER | str | Nome do jogador |
| POSIÇÃO | str | GK, ZAG, MEI, ATA |
| TIME | str | Time que o jogador representou na partida |
| ... | int | Estatísticas (GOL, ASS, STG, etc.) |
| PTS | int | Pontuação calculada |

---

## 📦 Localização do processamento no projeto

- Arquivo: `src/data_loader.py`
- Funções principais:
  - `carregar_dados_google_sheets()`
  - `tratar_dataframe(df)`

---

# ✨ Observações

- Em caso de alteração nos critérios de pontuação, basta atualizar o dicionário `CRITERIOS` no `data_loader.py`.
- O tratamento foi desenhado para ser **robusto**, lidando com dados faltantes e erros sem quebrar o dashboard.

