document.addEventListener("DOMContentLoaded", () => {
  const API_URL = "/categoria/";

  const form = document.getElementById("formCategoria");
  const lista = document.getElementById("listaCategoria");
  const nomeInput = document.getElementById("nome");
  const idInput = document.getElementById("idcategoria");
  const modalConfirmacao = document.getElementById("modal-confirmacao-categoria");
  const btnConfirmar = document.getElementById("btn-confirmar-categoria");
  const btnCancelar = document.getElementById("btn-cancelar-categoria");

  let idCategoriaParaExcluir = null;

  if (!form || !lista || !nomeInput || !idInput) return;

  function exibirMensagemCategoria(mensagem, sucesso = false) {
    if (typeof window.exibirMensagem === "function") {
      window.exibirMensagem(mensagem, sucesso);
      return;
    }

    const alerta = document.getElementById("alerta");
    if (!alerta) return;

    alerta.textContent = mensagem;
    alerta.className = sucesso ? "alert-success" : "alert-error";
    alerta.style.display = "block";

    setTimeout(() => {
      alerta.style.display = "none";
    }, 4000);
  }

  async function carregarCategorias() {
    const resposta = await fetch(`${API_URL}categorias`);
    const retorno = await resposta.json();
    const categorias = retorno.dados;

    lista.innerHTML = "";

    if (categorias) {
      categorias.forEach((categoria) => {
        lista.innerHTML += `
          <tr>
            <td>${categoria.id}</td>
            <td>${categoria.nome}</td>
            <td>
              <button type="button" class="btn-editar" data-editar-id="${categoria.id}">Editar</button>
              <button type="button" class="btn-excluir" data-excluir-id="${categoria.id}">Excluir</button>
            </td>
          </tr>
        `;
      });

      return;
    }

    exibirMensagemCategoria(retorno.mensagem || "Nenhuma categoria encontrada.");
  }

  async function editarCategoria(id) {
    const resposta = await fetch(`${API_URL}categoria/${id}`);
    const retorno = await resposta.json();
    const categoria = retorno.dados;

    if (!categoria) return;

    idInput.value = categoria.id;
    nomeInput.value = categoria.nome;
    nomeInput.focus();

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function mostrarModalCategoria(id) {
    idCategoriaParaExcluir = id;

    if (modalConfirmacao) {
      modalConfirmacao.style.display = "flex";
    }
  }

  async function excluirCategoria() {
    if (idCategoriaParaExcluir === null) return;

    const resposta = await fetch(`${API_URL}categoria/${idCategoriaParaExcluir}`, {
      method: "DELETE",
    });

    const retorno = await resposta.json();
    const msg = retorno.Mensagem || retorno.mensagem || "Erro ao excluir.";

    exibirMensagemCategoria(msg, retorno.Resultado);

    await carregarCategorias();

    idCategoriaParaExcluir = null;

    if (modalConfirmacao) {
      modalConfirmacao.style.display = "none";
    }
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const id = idInput.value;
    const nome = nomeInput.value.trim();

    if (!nome) {
      exibirMensagemCategoria("O campo 'Nome' é obrigatório.");
      return;
    }

    const metodo = id ? "PUT" : "POST";
    const endpoint = id ? "categoria" : "categorias";

    const resposta = await fetch(`${API_URL}${endpoint}`, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, nome }),
    });

    const retorno = await resposta.json();
    const msg = retorno.Mensagem || retorno.mensagem || "Erro ao salvar.";

    exibirMensagemCategoria(msg, retorno.Resultado);

    nomeInput.value = "";
    idInput.value = "";

    await carregarCategorias();
  });

  form.addEventListener("reset", (event) => {
    event.preventDefault();

    idInput.value = "";
    nomeInput.value = "";

    carregarCategorias();
  });

  lista.addEventListener("click", (event) => {
    const editarButton = event.target.closest("[data-editar-id]");
    const excluirButton = event.target.closest("[data-excluir-id]");

    if (editarButton) {
      editarCategoria(editarButton.dataset.editarId);
    }

    if (excluirButton) {
      mostrarModalCategoria(excluirButton.dataset.excluirId);
    }
  });

  if (btnConfirmar) {
    btnConfirmar.addEventListener("click", excluirCategoria);
  }

  if (btnCancelar) {
    btnCancelar.addEventListener("click", () => {
      idCategoriaParaExcluir = null;

      if (modalConfirmacao) {
        modalConfirmacao.style.display = "none";
      }
    });
  }

  carregarCategorias();
});