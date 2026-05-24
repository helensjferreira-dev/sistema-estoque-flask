async function carregarRelatorio() {
  const resp = await fetch("/relatorio/estoque/dados");
  const dados = await resp.json();
  const produtos = dados.dados || [];

  const tabela = document.getElementById("listaRelatorio");

  let nomes = [];
  let estoqueAtual = [];
  let estoqueMinimo = [];

  tabela.innerHTML = "";

  produtos.forEach((p) => {
    const valorEstoqueAtual = Number(p.estoque_atual ?? 0);
    const valorEstoqueMinimo = Number(p.estoque_minimo ?? 0);
    const categoriaNome = p.categoria_nome ?? "-";

    let statusClass = "ok";
    let statusTexto = "OK";

    if (valorEstoqueAtual <= 0) {
      statusClass = "falta";
      statusTexto = "Em falta";
    } else if (
      valorEstoqueMinimo > 0 &&
      valorEstoqueAtual < valorEstoqueMinimo
    ) {
      statusClass = "alerta";
      statusTexto = "Baixo";
    }

    tabela.innerHTML += `
      <tr>
        <td>${p.produto_id}</td>
        <td>${p.produto_nome}</td>
        <td>${categoriaNome}</td>
        <td>${valorEstoqueMinimo}</td>
        <td class="${statusClass}">${valorEstoqueAtual}</td>
        <td>
          <span class="status-badge ${statusClass}">
            ${statusClass === "ok" ? "✅" : statusClass === "alerta" ? "⚠️" : "🚫"}
            ${statusTexto}
          </span>
        </td>
      </tr>
    `;

    nomes.push(p.produto_nome);
    estoqueAtual.push(valorEstoqueAtual);
    estoqueMinimo.push(valorEstoqueMinimo);
  });

  const normalizados = produtos.map((p) => ({
    atual: Number(p.estoque_atual ?? 0),
    minimo: Number(p.estoque_minimo ?? 0),
  }));

  const totalProdutos = normalizados.length;
  const emFalta = normalizados.filter((x) => x.atual <= 0).length;
  const baixos = normalizados.filter(
    (x) => x.atual > 0 && x.minimo > 0 && x.atual < x.minimo,
  ).length;
  const ok = totalProdutos - emFalta - baixos;

  const percFalta =
    totalProdutos > 0 ? ((emFalta / totalProdutos) * 100).toFixed(1) : 0;
  const percBaixo =
    totalProdutos > 0 ? ((baixos / totalProdutos) * 100).toFixed(1) : 0;

  const resumoDiv = document.getElementById("resumo");

  resumoDiv.innerHTML = `
    <div class="summary-item">
      <span>Total de produtos</span>
      <strong>${totalProdutos}</strong>
    </div>
    <div class="summary-item danger">
      <span>Em falta</span>
      <strong>${emFalta} (${percFalta}%)</strong>
    </div>
    <div class="summary-item warning">
      <span>Baixo</span>
      <strong>${baixos} (${percBaixo}%)</strong>
    </div>
    <div class="summary-item success">
      <span>OK</span>
      <strong>${ok}</strong>
    </div>
  `;

  const ctx = document.getElementById("graficoEstoque").getContext("2d");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: nomes,
      datasets: [
        {
          label: "Estoque Atual",
          data: estoqueAtual,
          backgroundColor: "#4caf50",
          barThickness: 40,
        },
        {
          label: "Estoque Mínimo",
          data: estoqueMinimo,
          backgroundColor: "#f44336",
          barThickness: 40,
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
          text: "Comparativo Estoque Atual x Mínimo",
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
            color: "#334155",
            maxRotation: 45,
            minRotation: 45,
            font: {
              size: 12,
              weight: "500",
            },
          },
          grid: {
            display: false,
          },
        },

        y: {
          beginAtZero: true,
          ticks: {
            color: "#334155",
            font: {
              size: 12,
            },
          },
          grid: {
            color: "rgba(0,0,0,0.05)",
          },
        },
      },
    },
  });
}

carregarRelatorio();
