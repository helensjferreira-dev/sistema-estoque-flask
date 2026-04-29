# 📘 Manual do Usuário – Sistema de Gestão de Estoque

Este manual orienta o usuário na utilização do sistema de gestão de estoque, detalhando suas principais funcionalidades e relatórios disponíveis.

---

## 📖 Introdução
O sistema controla o estoque de forma **automática e exclusiva pelas movimentações de entrada e saída**.  
Não há ajustes manuais: cada alteração precisa ser registrada como uma movimentação.  
Isso garante rastreabilidade e consistência nos relatórios.

---

## 🔑 Acesso e Navegação
- Login obrigatório para acessar o sistema.
- Menu principal com opções de **Movimentações** e **Validade de Lotes**.
- Cada seção possui filtros, tabelas e botões de exportação.

---

## 📦 Movimentações
O controle de estoque é feito **exclusivamente pelas movimentações de entrada e saída**.  
Cada entrada ou saída altera o saldo de estoque e é registrada para auditoria.

### Funcionalidades
- **Filtros disponíveis**: período, produto, tipo, usuário.
- **Tabela de resultados**: ID, data, produto, categoria, tipo, quantidade, valor unitário, motivo, usuário, lote e estoque do lote.
- **Resumo automático**: entradas, saídas, saldo líquido e valor total movimentado.
- **Exportação**: PDF, CSV e Excel (XLSX).

---

## 🗓️ Validade de Lotes
Permite acompanhar a validade dos lotes em estoque.

### Funcionalidades
- **Tabela de resultados**: ID, produto, categoria, lote, quantidade, validade, dias restantes, status.
- **Status automático**:
  - Vencido (dias ≤ 0)
  - Próximo (dias ≤ 30)
  - OK (dias > 30)
- **Resumo gerencial**: total de lotes, vencidos e próximos.
- **Gráfico interativo**: dias restantes por lote, com cores indicativas (vermelho, laranja, verde).
- **Exportação**: PDF, CSV e Excel (XLSX).

---

## 🎨 Interface Visual
- Verde → Entradas / Lotes OK
- Vermelho → Saídas / Lotes vencidos
- Laranja → Lotes próximos do vencimento
- Cinza → Lotes esgotados

---

## 🛠️ Dicas de Uso
- Sempre utilize filtros de data para relatórios precisos.
- Exporte relatórios para compartilhar ou manter histórico.
- Consulte o resumo gerencial para visão rápida da situação.
- Use o gráfico de validade para identificar produtos que precisam de atenção.

---

## 📌 Conclusão
O sistema é uma ferramenta completa para **controle de estoque e validade de produtos**, permitindo:
- Registrar e acompanhar movimentações.
- Monitorar validade de lotes.
- Gerar relatórios detalhados em múltiplos formatos.
- Apoiar decisões de compra e gestão de estoque.
