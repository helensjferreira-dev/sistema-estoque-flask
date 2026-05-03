      const API_URL = "/usuario/";
      const form = document.getElementById("userForm");
      const nomeInput = document.getElementById("nome");
      const emailInput = document.getElementById("email");
      const senhaInput = document.getElementById("senha");
      const tabelaBody = document.querySelector("tbody");
      let idEditando = null;
      let idParaExcluir = null;

      // mensagem de alerta com cores padronizadas
      function exibirMensagem(mensagem, sucesso = false) {
        const alerta = document.getElementById("alerta");
        alerta.innerText = mensagem;
        alerta.style.display = "block";
        alerta.style.backgroundColor = sucesso ? "#d4edda" : "#f8d7da"; // verde ou vermelho
        alerta.style.color = sucesso ? "#155724" : "#721c24";
        alerta.style.border = sucesso
          ? "1px solid #c3e6cb"
          : "1px solid #f5c6cb";

        setTimeout(() => {
          alerta.style.display = "none";
        }, 4000);
      }

      // Carrega usuários na tabela
      async function carregarUsuarios() {
        const resposta = await fetch(API_URL + "usuarios");
        const retorno = await resposta.json();
        const usuarios = retorno.dados || [];

        tabelaBody.innerHTML = "";

        usuarios.forEach((usuario) => {
          const linha = document.createElement("tr");
          linha.innerHTML = `
            <td>${usuario.id}</td>
            <td>${usuario.nome}</td>
            <td>${usuario.email}</td>
            <td>
              <button class="btn-editar" onclick="editarUsuario(${usuario.id})">Editar</button>
              <button class="btn-excluir" onclick="mostrarModal(${usuario.id})">Excluir</button>
            </td>
          `;
          tabelaBody.appendChild(linha);
        });
      }

      // Validação e envio do formulário
      form.onsubmit = async (e) => {
        e.preventDefault();

        const nome = nomeInput.value.trim();
        const email = emailInput.value.trim();
        const senha = senhaInput.value.trim();

        if (!nome || !email || !senha) {
          exibirMensagem("Todos os campos são obrigatórios.", false);
          return;
        }
        // Verificação de e-mail duplicado (apenas no front)
  const respostaUsuarios = await fetch(API_URL + "usuarios");
  const retornoUsuarios = await respostaUsuarios.json();
  const usuariosExistentes = retornoUsuarios.dados || [];

  const emailJaExiste = usuariosExistentes.some(
    (u) => u.email.toLowerCase() === email.toLowerCase() && u.id !== idEditando
  );

        if (emailJaExiste) {
          exibirMensagem("Este e-mail já está cadastrado.", false);
          return; // interrompe o envio
        }

        const metodo = idEditando ? "PUT" : "POST";
        const url = idEditando ? API_URL + "usuario" : API_URL + "usuarios";

        const resposta = await fetch(url, {
          method: metodo,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: idEditando, nome, email, senha }),
        });

        const retorno = await resposta.json();
        const mensagem = retorno.Mensagem || "Erro ao salvar.";
        exibirMensagem(mensagem, retorno.Resultado);

        nomeInput.value = "";
        emailInput.value = "";
        senhaInput.value = "";
        idEditando = null;

        carregarUsuarios();
      };

      // Edita usuário
      async function editarUsuario(id) {
        const resposta = await fetch(API_URL + "usuario/" + id);
        const retorno = await resposta.json();
        const usuario = retorno.dados;

        if (usuario) {
          idEditando = usuario.id;
          nomeInput.value = usuario.nome;
          emailInput.value = usuario.email;
          senhaInput.value = usuario.senha;
          nomeInput.focus();
          // rola a página até o topo
          window.scrollTo({ top: 0, behavior: "smooth" });
        }
      }

      // Modal de confirmação
      function mostrarModal(id) {
        idParaExcluir = id;
        document.getElementById("modal-confirmacao").style.display = "flex";
      }

      document.getElementById("btn-confirmar").onclick = async () => {
        if (idParaExcluir !== null) {
          const resposta = await fetch(API_URL + "usuario/" + idParaExcluir, {
            method: "DELETE",
          });
          const retorno = await resposta.json();
          const mensagem = retorno.Mensagem || "Erro ao excluir.";
          exibirMensagem(mensagem, retorno.Resultado);
          carregarUsuarios();
          idParaExcluir = null;
        }
        document.getElementById("modal-confirmacao").style.display = "none";
      };

      document.getElementById("btn-cancelar").onclick = () => {
        idParaExcluir = null;
        document.getElementById("modal-confirmacao").style.display = "none";
      };

      // Reset do form
      form.onreset = async (e) => {
        e.preventDefault();
        idEditando = null;
        nomeInput.value = "";
        emailInput.value = "";
        senhaInput.value = "";
        exibirMensagem("Formulário limpo.", false);
        carregarUsuarios();
      };

      // Inicializando
      carregarUsuarios();