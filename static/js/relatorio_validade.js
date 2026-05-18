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
          <td>
  <span class="status-badge ${statusClass}">
    ${statusClass === "ok" ? "✅" : statusClass === "proximo" ? "⚠️" : "🚫"}
    ${l.status}
  </span>
</td>
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
  const seguros = totalLotes - vencidos - proximos;

  resumoDiv.className = "report-summary";
  resumoDiv.innerHTML = `
  <div class="summary-item">
    <span>Total de lotes</span>
    <strong>${totalLotes}</strong>
  </div>
  <div class="summary-item danger">
    <span>Vencidos</span>
    <strong>${vencidos}</strong>
  </div>
  <div class="summary-item warning">
    <span>Próximos do vencimento</span>
    <strong>${proximos}</strong>
  </div>
  <div class="summary-item success">
    <span>Seguros</span>
    <strong>${seguros}</strong>
  </div>
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
          barThickness: 32,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,

      plugins: {
        legend: {
          position: "top",
          labels: {
            color: "#334155",
            font: {
              size: 13,
              weight: "600",
              family: "Inter, sans-serif",
            },
            padding: 16,
            boxWidth: 18,
          },
        },

        title: {
          display: true,
          text: "Dias restantes para validade dos lotes",
          color: "#0f172a",
          font: {
            size: 18,
            weight: "700",
            family: "Inter, sans-serif",
          },
          padding: {
            bottom: 24,
          },
        },
      },

      scales: {
        x: {
          ticks: {
            color: "#475569",
            font: {
              size: 12,
              weight: "500",
            },
          },
          grid: {
            color: "#e2e8f0",
          },
        },

        y: {
          ticks: {
            color: "#475569",
            font: {
              size: 12,
            },
          },
          grid: {
            color: "#e2e8f0",
          },
        },
      },
    },
  });
}

carregarRelatorioValidade();
