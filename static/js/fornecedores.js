document.addEventListener("DOMContentLoaded", () => {
  const API_URL = "/fornecedor/";

  const form = document.getElementById("formFornecedor");
  const tabelaBody = document.getElementById("listaFornecedor");

  const nomeInput = document.getElementById("nome");
  const emailInput = document.getElementById("email");
  const telefoneInput = document.getElementById("telefone");

  const modal = document.getElementById("modal-confirmacao-fornecedor");
  const btnConfirmar = document.getElementById("btn-confirmar-fornecedor");
  const btnCancelar = document.getElementById("btn-cancelar-fornecedor");

  let idEditando = null;
  let idParaExcluir = null;

  if (!form || !tabelaBody) return;

  function showMessage(msg, success = false) {
    if (window.exibirMensagem) {
      window.exibirMensagem(msg, success);
    }
  }

  async function carregar() {
    const resp = await fetch(API_URL + "fornecedores");
    const data = await resp.json();

    tabelaBody.innerHTML = "";

    data.dados?.forEach((f) => {
      tabelaBody.innerHTML += `
        <tr>
          <td>${f.id}</td>
          <td>${f.nome}</td>
          <td>${f.email ?? "-"}</td>
          <td>${f.telefone ?? "-"}</td>
          <td>
            <button type="button" data-editar="${f.id}" class="btn-editar">Editar</button>
            <button type="button" data-excluir="${f.id}" class="btn-excluir">Excluir</button>
          </td>
        </tr>
      `;
    });
  }

  async function editar(id) {
    const resp = await fetch(API_URL + "fornecedor/" + id);
    const data = await resp.json();

    const f = data.dados;

    if (!f) return;

    idEditando = f.id;
    nomeInput.value = f.nome;
    emailInput.value = f.email;
    telefoneInput.value = f.telefone;

    nomeInput.focus();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function abrirModal(id) {
    idParaExcluir = id;
    modal.style.display = "flex";
  }

  async function excluir() {
    if (!idParaExcluir) return;

    const resp = await fetch(API_URL + "fornecedor/" + idParaExcluir, {
      method: "DELETE",
    });

    const data = await resp.json();

    showMessage(data.Mensagem || data.mensagem, data.Resultado);

    idParaExcluir = null;
    modal.style.display = "none";

    carregar();
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = nomeInput.value.trim();
    const email = emailInput.value.trim() || null;
    const telefone = telefoneInput.value.trim() || null;

    if (!nome) {
      showMessage("O campo Nome é obrigatório.");
      return;
    }

    const respLista = await fetch(API_URL + "fornecedores");
    const lista = await respLista.json();

    const duplicado = lista.dados?.some(
      (f) =>
        f.nome.toLowerCase() === nome.toLowerCase() &&
        f.id !== idEditando
    );

    if (duplicado) {
      showMessage("Já existe um fornecedor com este nome.");
      return;
    }

    const metodo = idEditando ? "PUT" : "POST";
    const endpoint = idEditando ? "fornecedor" : "fornecedores";

    const resp = await fetch(API_URL + endpoint, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: idEditando, nome, email, telefone }),
    });

    const data = await resp.json();

    showMessage(data.Mensagem || data.mensagem, data.Resultado);

    form.reset();
    idEditando = null;

    carregar();
  });

  tabelaBody.addEventListener("click", (e) => {
    const editBtn = e.target.closest("[data-editar]");
    const delBtn = e.target.closest("[data-excluir]");

    if (editBtn) editar(editBtn.dataset.editar);
    if (delBtn) abrirModal(delBtn.dataset.excluir);
  });

  btnConfirmar?.addEventListener("click", excluir);

  btnCancelar?.addEventListener("click", () => {
    idParaExcluir = null;
    modal.style.display = "none";
  });

  carregar();
});