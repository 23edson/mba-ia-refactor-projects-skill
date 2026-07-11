**NOTA IMPORTANTE:** Este relatório deve ser salvo em um arquivo com o nome `audit-project-N.md`, onde `N` é o número do projeto (1, 2 ou 3). Nenhum outro formato de nome de arquivo é permitido.

# Template de Relatório de Auditoria

Use este template exatamente ao gerar o relatório da Fase 2. Substitua os placeholders pelos valores reais encontrados.

---

```
╔══════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE AUDITORIA ARQUITETURAL                ║
╚══════════════════════════════════════════════════════════════╝

Projeto:    <nome do projeto>
Stack:      <linguagem> + <framework>
Data:       <data atual>
Total de findings: <N>

┌─────────────────────────────────────────────────────────────┐
│  CRITICAL: <N>  │  HIGH: <N>  │  MEDIUM: <N>  │  LOW: <N>  │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════
 🔴 CRITICAL
═══════════════════════════════════

[C-1] <Nome do Anti-Pattern> (AP-XX)
  Arquivo: <arquivo>:<linha>
  Descrição: <descrição do que está errado no código>
  Código:
    <trecho exato do código problemático>
  Impacto: <descrição do impacto específico neste projeto>
  Recomendação: <ação concreta para resolver o problema>

[C-2] <Nome do Anti-Pattern> (AP-XX)
  Arquivo: <arquivo>:<linha>
  Descrição: <descrição do que está errado no código>
  Código:
    <trecho exato do código problemático>
  Impacto: <descrição do impacto específico neste projeto>
  Recomendação: <ação concreta para resolver o problema>

═══════════════════════════════════
 🟠 HIGH
═══════════════════════════════════

[H-1] <Nome do Anti-Pattern> (AP-XX)
  Arquivo: <arquivo>:<linha>
  Descrição: <descrição do que está errado no código>
  Código:
    <trecho exato do código problemático>
  Impacto: <descrição do impacto específico neste projeto>
  Recomendação: <ação concreta para resolver o problema>

═══════════════════════════════════
 🟡 MEDIUM
═══════════════════════════════════

[M-1] <Nome do Anti-Pattern> (AP-XX)
  Arquivo: <arquivo>:<linha>
  Descrição: <descrição do que está errado no código>
  Código:
    <trecho exato do código problemático>
  Impacto: <descrição do impacto específico neste projeto>
  Recomendação: <ação concreta para resolver o problema>

═══════════════════════════════════
 🔵 LOW
═══════════════════════════════════

[L-1] <Nome do Anti-Pattern> (AP-XX)
  Arquivo: <arquivo>:<linha>
  Descrição: <descrição do que está errado no código>
  Código:
    <trecho exato do código problemático>
  Impacto: <descrição do impacto específico neste projeto>
  Recomendação: <ação concreta para resolver o problema>

═══════════════════════════════════
 RESUMO DE AÇÕES NECESSÁRIAS
═══════════════════════════════════

CRITICAL (corrigir antes de qualquer deploy):
  - [ ] <ação concreta para C-1>
  - [ ] <ação concreta para C-2>

HIGH (corrigir nesta sprint):
  - [ ] <ação concreta para H-1>

MEDIUM (planejar para próxima sprint):
  - [ ] <ação concreta para M-1>

LOW (melhorias incrementais):
  - [ ] <ação concreta para L-1>
```

---

## Regras de Preenchimento

1. **Arquivo e linha são obrigatórios** — nunca deixe como "arquivo.py" sem número de linha.
2. **Código** — copie o trecho real, não uma descrição. Máximo 3-5 linhas para manter o relatório legível.
3. **Impacto** — descreva o impacto *no contexto deste projeto*, não genericamente. Ex: "permite que qualquer usuário acesse dados financeiros de todos os clientes" em vez de "viola segurança".
4. **Ordenação** — sempre CRITICAL primeiro, depois HIGH, MEDIUM, LOW. Dentro de cada categoria, ordene por arquivo/linha.
5. **IDs** — use [C-1], [C-2], [H-1], etc. para referenciar findings na Fase 3.
6. **APIs deprecated** — inclua na categoria LOW com referência ao AP-15, listando a API atual e a substituta recomendada.
7. **Não invente findings** — se não há nenhum finding CRITICAL, omita essa seção. Honestidade é mais útil que completude forçada.