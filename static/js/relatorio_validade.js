async function carregarRelatorioValidade() {
  const resp = await fetch("/relatorio/validade/dados");
  const dados = await resp.json();
  const lotes = dados.dados || [];
  const tabela = document.getElementById("listaValidade");

  let nomes = [];
  let diasRestantes = [];

  tabela.innerHTML = "";
  lotes.forEach((l) => {
    let statusClass = "ok";
    if (l.status === "Vencido") {
      statusClass = "vencido";
    } else if (l.status === "Próximo") {
      statusClass = "proximo";
    }

    tabela.innerHTML += `
        <tr>
          <td>${l.id}</td>
          <td>${l.produto_nome}</td>
          <td>${l.categoria_nome}</td>
          <td>${l.numero}</td>
          <td>${l.quantidade}</td>
          <td>${l.validade}</td>
          <td>${l.dias_restantes}</td>
          <td class="${statusClass}">${l.status}</td>
        </tr>
      `;
    nomes.push(l.produto_nome + " (Lote " + l.numero + ")");
    diasRestantes.push(l.dias_restantes);
  });

  // Resumo gerencial
  let totalLotes = lotes.length;
  let vencidos = lotes.filter((l) => l.dias_restantes <= 0).length;
  let proximos = lotes.filter(
    (l) => l.dias_restantes > 0 && l.dias_restantes <= 30,
  ).length;
  let resumoDiv = document.getElementById("resumoValidade");

  // Definir cor
  let resumoClasse = "resumo-verde";
  if (vencidos > 0) {
    resumoClasse = "resumo-vermelho";
  } else if (proximos > 0) {
    resumoClasse = "resumo-laranja";
  }
  resumoDiv.className = resumoClasse;
  resumoDiv.innerHTML = `
          Total de lotes: ${totalLotes} <br>
          Vencidos: ${vencidos} <br>
          Próximos do vencimento (≤30 dias): ${proximos}
        `;

  // Gráfico
  const ctx = document.getElementById("graficoValidade").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: nomes,
      datasets: [
        {
          label: "Dias restantes",
          data: diasRestantes,
          backgroundColor: diasRestantes.map((d) =>
            d <= 0 ? "red" : d <= 30 ? "orange" : "green",
          ),
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: {
          display: true,
          text: "Dias restantes para validade dos lotes",
        },
      },
    },
  });
}

carregarRelatorioValidade();
