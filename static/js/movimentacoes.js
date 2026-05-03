      const API_URL = "/movimentacao/";
      const form = document.getElementById("movForm");
      const tabelaBody = document.getElementById("listaMov");
      const produtoInput = document.getElementById("produto");
      const usuarioHidden = document.getElementById("usuario");

      const idInput = document.getElementById("idmov");
      const alerta = document.getElementById("alerta");
      let idMovParaExcluir = null;

      const loteInput = document.getElementById("lote-numero");
      const categoriaHidden = document.getElementById("categoria");

      loteInput.addEventListener("blur", async () => {
        const numero = loteInput.value.trim();
        if (!numero) return;

        try {
          const resp = await fetch(`/lote/por-numero/${numero}`);
          const retorno = await resp.json();
          console.log("Retorno lote:", retorno);

          const ok =
            retorno.Resultado === undefined
              ? !!retorno.dados
              : retorno.Resultado;
          const lote = retorno.dados;

          if (ok && lote) {
            produtoInput.value = lote.nome_produto;
            document.getElementById("idproduto").value = lote.idproduto; // guarda id

            categoriaHidden.value = lote.idcategoria;
          } else {
            exibirMensagem(retorno.Mensagem || "Lote não encontrado.");
          }
        } catch (erro) {
          console.error("Erro ao buscar lote:", erro);
          exibirMensagem("Erro ao buscar lote.");
        }
      });

      function exibirMensagem(msg, sucesso = false) {
        alerta.textContent = msg;
        alerta.style.display = "block";
        alerta.style.backgroundColor = sucesso ? "#d4edda" : "#f8d7da";
        alerta.style.color = sucesso ? "#155724" : "#721c24";
        clearTimeout(alerta._timer);
        alerta._timer = setTimeout(() => (alerta.style.display = "none"), 3500);
      }

      async function carregarProdutos() {
        try {
          const resp = await fetch("/produto/produtos");
          const j = await resp.json();
          const produtos = j.dados || [];

          window.listaProdutos = produtos;
        } catch (e) {
          console.error("Erro carregar produtos:", e);
          exibirMensagem("Erro ao carregar produtos.");
        }
      }

      function formatarDataISO(dataISO) {
        if (!dataISO) return "-";
        const partes = dataISO.split("-");
        if (partes.length !== 3) return dataISO; // se não vier no formato esperado
        return `${partes[2]}/${partes[1]}/${partes[0]}`; // dd/mm/yyyy
      }
      async function carregarMovimentacoes() {
        try {
          const resp = await fetch(API_URL + "movimentacoes");
          const j = await resp.json();
          const movs = (j.dados || []).slice().reverse();
          tabelaBody.innerHTML = "";
          movs.forEach((m) => {
            const id = m.idmovimentacao ?? m.IDMOVIMENTACAO ?? "-";
            const nome_produto = m.nome_produto || "-";
            const nome_categoria = m.nome_categoria || "-";
            const motivo = m.motivo ?? "-";
            const quantidade = m.quantidade ?? "-";
            const valor = m.valor_unitario ?? null;
            const nome_usuario = m.nome_usuario || "-";
            const tr = document.createElement("tr");
            tr.dataset.produto = m.idproduto ?? "";
            tr.dataset.tipo = m.tipo ?? "";
            tr.dataset.usuario = m.nome_usuario?.toLowerCase() ?? "";
            tr.dataset.data = m.data_movimentacao ?? "";

            tr.innerHTML = `
        <td>${id}</td>
        <td>${nome_produto}</td>
        <td>${nome_categoria}</td>
        <td>${motivo}</td>
        <td>${quantidade}</td>
        <td>${valor !== null ? Number(valor).toFixed(2) : "-"}</td>
        <td>${nome_usuario}</td>
        <td>${formatarDataISO(m.data_movimentacao)}</td>

        <td>
          <button type="button" data-id="${id}" class="btn-editar">Editar</button>
          <button type="button" data-id="${id}" class="btn-excluir">Excluir</button>
        </td>
      `;
            tabelaBody.appendChild(tr);
          });
          tabelaBody.querySelectorAll(".btn-editar").forEach((btn) => {
            btn.onclick = () => editarMovimentacao(btn.dataset.id);
          });
          tabelaBody.querySelectorAll(".btn-excluir").forEach((btn) => {
            btn.onclick = () => mostrarModalMov(btn.dataset.id);
          });
        } catch (e) {
          console.error("Erro carregar movimentações:", e);
          exibirMensagem("Erro ao carregar movimentações.");
        }
      }
      function aplicarFiltrosMov() {
        const produto = document.getElementById("filtro-produto").value;
        const tipo = document.getElementById("filtro-tipo").value;
        const usuario = document
          .getElementById("filtro-usuario")
          .value.toLowerCase();
        const data = document.getElementById("filtro-data").value;
        const busca = document.getElementById("buscaMov").value.toLowerCase();

        const linhas = tabelaBody.querySelectorAll("tr");
        linhas.forEach((linha) => {
          const texto = linha.innerText.toLowerCase();
          const idProdutoLinha = linha.dataset.produto;
          const tipoLinha = linha.dataset.tipo;
          const usuarioLinha = linha.dataset.usuario;
          const dataLinha = linha.dataset.data;

          let visivel = true;
          if (produto && idProdutoLinha !== produto) visivel = false;
          if (tipo && tipoLinha !== tipo) visivel = false;
          if (usuario && !usuarioLinha.includes(usuario)) visivel = false;
          if (data && dataLinha !== data) visivel = false;
          if (busca && !texto.includes(busca)) visivel = false;

          linha.style.display = visivel ? "" : "none";
        });
      }
      async function carregarProdutosFiltro() {
        const resp = await fetch("/produto/produtos");
        const dados = await resp.json();
        const combo = document.getElementById("filtro-produto");
        combo.innerHTML = `<option value="">Todos</option>`;
        dados.dados?.forEach((p) => {
          combo.innerHTML += `<option value="${p.id}">${p.nome}</option>`;
        });
      }

      form.onsubmit = async (ev) => {
        ev.preventDefault();
        const id = idInput.value || null;
        const data_movimentacao = document.getElementById("dt-mov").value;
        const idusuario = usuarioHidden.value;
        const idproduto = document.getElementById("idproduto").value;

        const tipo = document.getElementById("tipo-mov").value;
        const quantidade = document.getElementById("qtd-mov").value;
        const valor_unitario = document.getElementById("valor-unitario").value;
        const motivo = document.getElementById("motivo").value;
        const numeroLote = document.getElementById("lote-numero").value;

        if (
          !data_movimentacao ||
          !idusuario ||
          !idproduto ||
          !tipo ||
          !quantidade
        ) {
          exibirMensagem("Preencha os campos obrigatórios.");
          return;
        }

        try {
          const respLote = await fetch(
            `/lote/por-numero/${encodeURIComponent(numeroLote)}`,
          );
          const jlote = await respLote.json();
          if (!jlote.dados) {
            exibirMensagem(jlote.Mensagem || "Número de lote inválido.");
            return;
          }
          const idlote = jlote.dados.idlote ?? jlote.dados.id;
          const metodo = id ? "PUT" : "POST";
          const endpoint = id ? "movimentacao" : "movimentacoes";

          const payload = {
            id,
            idlote,
            idusuario,
            idproduto,
            data_movimentacao,
            tipo,
            quantidade,
            valor_unitario,
            motivo,
          };

          const resp = await fetch(API_URL + endpoint, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          });

          const r = await resp.json();
          exibirMensagem(
            r.Mensagem || r.mensagem || "Operação realizada.",
            r.Resultado,
          );

          if (r.Resultado) {
            await carregarMovimentacoes();
            form.reset();
            idInput.value = "";
            produtoInput.value = "";
            document.getElementById("tipo-mov").value = "";
            document.getElementById("valor-unitario").value = "";
            document.getElementById("motivo").value = "";
            document.getElementById("lote-numero").value = "";
            document.getElementById("qtd-mov").value = "";
          }
        } catch (e) {
          console.error("Erro salvar movimentação:", e);
          exibirMensagem("Erro ao salvar movimentação.");
        }
      };

      async function editarMovimentacao(id) {
        try {
          const resp = await fetch(API_URL + "movimentacao/" + id);
          const r = await resp.json();
          const m = r.dados;
          if (!m) {
            exibirMensagem(r.Mensagem || "Movimentação não encontrada.");
            return;
          }

          idInput.value = m.idmovimentacao ?? m.IDMOVIMENTACAO ?? "";
          document.getElementById("dt-mov").value = m.data_movimentacao ?? "";
          usuarioHidden.value = m.idusuario ?? usuarioHidden.value;

          const idProd = m.idproduto ?? "";
          const nomeProd = m.nome_produto ?? "";
          if (idProd) {
            document.getElementById("idproduto").value = idProd; // guarda ID
            produtoInput.value = nomeProd; // mostra nome
          }

          document.getElementById("lote-numero").value = m.numero_lote ?? "";
          document.getElementById("qtd-mov").value = m.quantidade ?? "";
          document.getElementById("tipo-mov").value = m.tipo ?? "";
          document.getElementById("valor-unitario").value =
            m.valor_unitario ?? "";
          document.getElementById("motivo").value = m.motivo ?? "";
          console.log("Dados da movimentação:", m);

          // foco no primeiro campo editável
          document.getElementById("dt-mov").focus();
          window.scrollTo({ top: 0, behavior: "smooth" });
        } catch (e) {
          console.error("Erro editar movimentação:", e);
          exibirMensagem("Erro ao carregar movimentação.");
        }
      }

      /* ------------------------------ MODAL EXCLUSÃO ------------------------------ */
      function mostrarModalMov(id) {
        idMovParaExcluir = id;
        document.getElementById("modal-confirmacao-mov").style.display = "flex";
      }

      document.getElementById("btn-confirmar-mov").onclick = async () => {
        if (idMovParaExcluir !== null) {
          try {
            const resp = await fetch(
              API_URL + "movimentacao/" + idMovParaExcluir,
              { method: "DELETE" },
            );
            const r = await resp.json();
            exibirMensagem(r.Mensagem || "Excluído.", r.Resultado);
            await carregarMovimentacoes();
          } catch (e) {
            console.error("Erro excluir movimentação:", e);
            exibirMensagem("Erro ao excluir movimentação.");
          }
          idMovParaExcluir = null;
        }
        document.getElementById("modal-confirmacao-mov").style.display = "none";
      };

      document.getElementById("btn-cancelar-mov").onclick = () => {
        idMovParaExcluir = null;
        document.getElementById("modal-confirmacao-mov").style.display = "none";
      };

      form.onreset = async (e) => {
        e.preventDefault();
        form.reset();
        idInput.value = "";
        produtoInput.value = "";
        document.getElementById("idproduto").value = "";

        document.getElementById("tipo-mov").value = "";
        document.getElementById("valor-unitario").value = "";
        document.getElementById("motivo").value = "";
        document.getElementById("lote-numero").value = "";
        document.getElementById("qtd-mov").value = "";
        await carregarMovimentacoes();
      };
      // Define o limite máximo do calendário como a data de hoje
      document.addEventListener("DOMContentLoaded", () => {
        const hoje = new Date().toISOString().split("T")[0];
        document.getElementById("dt-mov").setAttribute("max", hoje);
      });
      document
        .querySelectorAll(
          "#filtro-produto, #filtro-tipo, #filtro-usuario, #filtro-data, #buscaMov",
        )
        .forEach((el) => el.addEventListener("input", aplicarFiltrosMov));

      (async function init() {
        await carregarProdutos();
        await carregarMovimentacoes();
        await carregarProdutosFiltro(); // para preencher o filtro de produtos
      })();