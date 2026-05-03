      const API_URL = "/produto/";
      const form = document.getElementById("formProduto");
      const tabelaBody = document.getElementById("listaProduto");
      const idInput = document.getElementById("idproduto");

      // Campos do form
      const nomeInput = document.getElementById("nome");
      const categoriaInput = document.getElementById("categoria");
      const descricaoInput = document.getElementById("descricao");
      const checkboxInput = document.getElementById("checkbox");
      const qtdMinInput = document.getElementById("qtd-min");

      // Alerta
      const alerta = document.getElementById("alerta");

      function exibirMensagem(mensagem, sucesso = false) {
        alerta.textContent = mensagem;
        alerta.style.display = "block";
        alerta.style.backgroundColor = sucesso ? "#d4edda" : "#f8d7da";
        alerta.style.color = sucesso ? "#155724" : "#721c24";
        alerta.style.border = sucesso
          ? "1px solid #c3e6cb"
          : "1px solid #f5c6cb";

        setTimeout(() => {
          alerta.style.display = "none";
        }, 4000);
      }

      // Carregar categorias no select
      async function carregarCategorias() {
        try {
          const resposta = await fetch("/categoria/categorias");
          const retorno = await resposta.json();
          const categorias = retorno.dados;

          categoriaInput.innerHTML =
            '<option value="">Selecione uma categoria</option>';

          if (categorias && categorias.length > 0) {
            categorias.forEach((cat) => {
              categoriaInput.innerHTML += `<option value="${cat.id}">${cat.nome}</option>`;
            });
          }
        } catch (erro) {
          console.error("Erro ao carregar categorias:", erro);
          exibirMensagem("Erro ao carregar categorias.");
        }
      }

      // Carregar produtos na tabela
      async function carregarProdutos() {
        try {
          const resposta = await fetch(API_URL + "produtos");
          const retorno = await resposta.json();
          const produtos = Array.isArray(retorno.dados) ? retorno.dados : [];

          tabelaBody.innerHTML = "";

          if (produtos && produtos.length > 0) {
            produtos.forEach((p) => {
              // Verifica se estoque está abaixo do mínimo
              let classeEstoque = "";
              if (
                p.estoque_minimo != null &&
                p.estoque_atual < p.estoque_minimo
              ) {
                classeEstoque = "alerta"; // classe CSS para destacar
              } else {
                classeEstoque = "ok"; 
              }
              // Normaliza valores nulos para exibição
              const descricao = p.descricao != null ? p.descricao : "-";
              const estoqueMinimo =
                p.estoque_minimo != null ? p.estoque_minimo : 0; // ou "-"
              const estoqueAtual =
                p.estoque_atual != null ? p.estoque_atual : "-";
              tabelaBody.innerHTML += `
                <tr>
                  <td>${p.id}</td>
                  <td>${p.nome}</td>
                  <td>${p.categoria?.nome ?? "-"}</td>
                  <td>${descricao}</td>
                  <td class="${classeEstoque}">${estoqueAtual}</td>
                  <td>
                    <button class="btn-editar" onclick="editarProduto(${
                      p.id
                    })">Editar</button>
                    <button class="btn-excluir" onclick="mostrarModalProduto(${
                      p.id
                    })">Excluir</button>
                  </td>
                </tr>
              `;
            });
          } else {
            exibirMensagem("Nenhum produto encontrado.");
          }
        } catch (erro) {
          console.error("Erro ao carregar produtos:", erro);
          exibirMensagem("Erro ao carregar produtos.");
        }
      }

      // Salvar ou atualizar produto
      form.onsubmit = async (e) => {
        e.preventDefault();

        const id = idInput.value;
        const nome = nomeInput.value.trim();
        const idcategoria = categoriaInput.value;
        const descricaoRaw = descricaoInput.value.trim();
        const controle_validade = checkboxInput.checked;
        const estoqueMinRaw = qtdMinInput.value;

        // obrigatórios: apenas nome e categoria
        if (!nome || !idcategoria) {
          exibirMensagem("Preencha os campos obrigatórios: Nome e Categoria");
          return;
        }
        // se campo estiver vazio, envia null
        const descricao = descricaoRaw === "" ? null : descricaoRaw;
        const estoque_minimo = estoqueMinRaw === "" ? null : estoqueMinRaw;

        const metodo = id ? "PUT" : "POST";
        const endpoint = id ? "produto" : "produtos";

        try {
          const resposta = await fetch(API_URL + endpoint, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              id,
              idcategoria,
              nome,
              descricao,
              controle_validade,
              estoque_minimo,
            }),
          });

          const retorno = await resposta.json();
          exibirMensagem(retorno.Mensagem || "Erro ao salvar.", true);

          form.reset();
          idInput.value = "";
          categoriaInput.value = "";
          checkboxInput.checked = false;

          carregarProdutos();
        } catch (erro) {
          console.error("Erro ao salvar produto:", erro);
          exibirMensagem("Erro na comunicação com o servidor.");
        }
      };

      // Editar produto
      async function editarProduto(id) {
        try {
          const resposta = await fetch(API_URL + "produto/" + id);
          const retorno = await resposta.json();
          const produto = retorno.dados;

          if (produto) {
            idInput.value = produto.id;
            nomeInput.value = produto.nome;
            categoriaInput.value = produto.idcategoria;
            descricaoInput.value = produto.descricao;
            checkboxInput.checked = produto.controle_validade;
            qtdMinInput.value = produto.estoque_minimo;
            nomeInput.focus();
            // rola a página até o topo
            window.scrollTo({ top: 0, behavior: "smooth" });
          }
        } catch (erro) {
          console.error("Erro ao editar produto:", erro);
          exibirMensagem("Erro ao carregar produto para edição.");
        }
      }

      // Modal de confirmação para exclusão
      let idProdutoParaExcluir = null;

      function mostrarModalProduto(id) {
        idProdutoParaExcluir = id;
        document.getElementById("modal-confirmacao-produto").style.display =
          "flex";
      }

      document.getElementById("btn-confirmar-produto").onclick = async () => {
        if (idProdutoParaExcluir !== null) {
          try {
            const resposta = await fetch(
              API_URL + "produto/" + idProdutoParaExcluir,
              {
                method: "DELETE",
              }
            );
            const retorno = await resposta.json();
            exibirMensagem(
              retorno.Mensagem || "Erro ao excluir.",
              retorno.Resultado
            );
            carregarProdutos();
          } catch (erro) {
            console.error("Erro ao excluir produto:", erro);
            exibirMensagem("Erro na comunicação com o servidor.");
          }
          idProdutoParaExcluir = null;
        }
        document.getElementById("modal-confirmacao-produto").style.display =
          "none";
      };

      document.getElementById("btn-cancelar-produto").onclick = () => {
        idProdutoParaExcluir = null;
        document.getElementById("modal-confirmacao-produto").style.display =
          "none";
      };

      // Reset do form
      form.onreset = (e) => {
        idInput.value = "";
        form.reset();
        categoriaInput.value = "";
        checkboxInput.checked = false;
        carregarProdutos();
      };

      // Inicializando
      carregarCategorias();
      carregarProdutos();