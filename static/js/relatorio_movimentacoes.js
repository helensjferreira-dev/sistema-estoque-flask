function formatarNumero(num) {
  const n = Number(num);
  return Number.isFinite(n) ? n.toLocaleString("pt-BR") : "-";
}

function formatarMoeda(valor) {
  const n = Number(valor);
  return Number.isFinite(n)
    ? n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })
    : "-";
}

function formatarData(dataStr) {
  if (!dataStr) return "-";

  const [data, hora] = dataStr.split("T");
  const [ano, mes, dia] = data.split("-");

  if (!hora) return `${dia}/${mes}/${ano}`;

  const horaFormatada = hora.slice(0, 5);

  return `${dia}/${mes}/${ano} ${horaFormatada}`;
}

function exportar(tipo) {
  const inicio = document.getElementById("dataInicio").value;
  const fim = document.getElementById("dataFim").value;
  const produto = document.getElementById("filtroProduto").value;
  const tipoMov = document.getElementById("filtroTipo").value;
  const usuario = document.getElementById("filtroUsuario").value;

  let url = `/relatorio/movimentacoes/export/${tipo}?data_inicio=${inicio}&data_fim=${fim}&produto=${produto}&tipo=${tipoMov}&usuario=${usuario}`;
  window.open(url, "_blank");
}

async function carregarRelatorio() {
  const inicio = document.getElementById("dataInicio").value;
  const fim = document.getElementById("dataFim").value;
  const produto = document.getElementById("filtroProduto").value;
  const tipo = document.getElementById("filtroTipo").value;
  const usuario = document.getElementById("filtroUsuario").value;

  const resp = await fetch(
    `/relatorio/movimentacoes?data_inicio=${inicio}&data_fim=${fim}&produto=${produto}&tipo=${tipo}&usuario=${usuario}`,
  );
  const dados = await resp.json();
  const lista = document.getElementById("listaMovPeriodo");
  lista.innerHTML = "";

  let entradas = 0;
  let saidas = 0;
  let valorTotal = 0;

  dados.dados.forEach((m) => {
    const qtd = Number(m.quantidade) || 0;
    const vu = m.valor_unitario != null ? Number(m.valor_unitario) : null;
    const tipo = (m.tipo || "").toLowerCase();

    let tipoClass = tipo === "entrada" ? "entrada" : "saida";
    let statusClass = "";
    if (m.status && m.status.includes("esgotado")) statusClass = "esgotado";

    lista.innerHTML += `
            <tr>
              <td>${m.idmovimentacao}</td>
              <td>${formatarData(m.data_movimentacao)}</td>
              <td>${m.produto}</td>
              <td>${m.categoria}</td>
              <td class="${tipoClass}">${m.tipo}</td>
              <td>${formatarNumero(qtd)}</td>
              <td>${vu != null ? formatarMoeda(vu) : "-"}</td>
              <td>${m.motivo ?? "-"}</td>
              <td>${m.usuario}</td>
              <td>${m.idlote ?? "-"}</td>
              <td>${formatarNumero(m.estoque_lote ?? 0)}</td>
            </tr>
          `;

    if (tipo === "entrada") entradas += qtd;
    if (tipo === "saida") saidas += qtd;
    if (vu != null) valorTotal += vu * qtd;
  });

  document.getElementById("resumoPeriodo").innerHTML = `
  <div class="summary-item success">
    <span>Entradas</span>
    <strong>${formatarNumero(entradas)}</strong>
  </div>

  <div class="summary-item danger">
    <span>Saídas</span>
    <strong>${formatarNumero(saidas)}</strong>
  </div>

  <div class="summary-item">
    <span>Saldo líquido</span>
    <strong>${formatarNumero(entradas - saidas)}</strong>
  </div>

  <div class="summary-item warning">
    <span>Valor total movimentado</span>
    <strong>${formatarMoeda(valorTotal)}</strong>
  </div>
`;
}

window.onload = () => {
  const hoje = new Date();
  const fim = hoje.toISOString().split("T")[0];
  const inicio = new Date(hoje.getTime() - 30 * 24 * 60 * 60 * 1000)
    .toISOString()
    .split("T")[0];
  document.getElementById("dataInicio").value = inicio;
  document.getElementById("dataFim").value = fim;
  carregarRelatorio();
};
