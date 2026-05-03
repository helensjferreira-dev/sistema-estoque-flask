document.addEventListener("DOMContentLoaded", () => {
  setupSidebar();
  setupLogoutModal();
  setupGlobalAlert();
});

function setupSidebar() {
  const sidebarToggle = document.querySelector(".sidebar-toggle");
  const sidebar = document.querySelector(".app-sidebar");

  if (!sidebarToggle || !sidebar) return;

  sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("ativo");
  });
}

function setupLogoutModal() {
  const logoutLink = document.getElementById("logoutLink");
  const modalLogout = document.getElementById("modal-logout");
  const modalFeedbackLogout = document.getElementById("modal-feedback-logout");
  const mensagemFeedbackLogout = document.getElementById("mensagem-feedback-logout");
  const btnConfirmarLogout = document.getElementById("btn-confirmar-logout");
  const btnCancelarLogout = document.getElementById("btn-cancelar-logout");
  const btnOkLogout = document.getElementById("btn-ok-logout");

  if (
    !logoutLink ||
    !modalLogout ||
    !modalFeedbackLogout ||
    !mensagemFeedbackLogout ||
    !btnConfirmarLogout ||
    !btnCancelarLogout ||
    !btnOkLogout
  ) {
    return;
  }

  logoutLink.addEventListener("click", (event) => {
    event.preventDefault();
    modalLogout.style.display = "flex";
  });

  btnCancelarLogout.addEventListener("click", () => {
    modalLogout.style.display = "none";
  });

  btnConfirmarLogout.addEventListener("click", async () => {
    try {
      const resposta = await fetch("/usuario/logoff", { method: "GET" });

      if (resposta.ok) {
        const retorno = await resposta.json();
        const mensagem = retorno.Mensagem || "Sessão finalizada com sucesso.";

        mensagemFeedbackLogout.innerText = mensagem;
        modalFeedbackLogout.style.display = "flex";

        btnOkLogout.onclick = () => {
          modalFeedbackLogout.style.display = "none";
          window.location.href = "/";
        };
      } else {
        let mensagemErro = `Erro ao sair. Status: ${resposta.status}`;

        try {
          const retorno = await resposta.json();
          mensagemErro = retorno.Mensagem || mensagemErro;
        } catch {}

        mensagemFeedbackLogout.innerText = mensagemErro;
        modalFeedbackLogout.style.display = "flex";

        btnOkLogout.onclick = () => {
          modalFeedbackLogout.style.display = "none";
        };
      }
    } catch (error) {
      mensagemFeedbackLogout.innerText =
        "Erro ao conectar com o servidor para deslogar.";
      modalFeedbackLogout.style.display = "flex";

      btnOkLogout.onclick = () => {
        modalFeedbackLogout.style.display = "none";
      };

      console.error("Erro no logoff:", error);
    }

    modalLogout.style.display = "none";
  });
}

function setupGlobalAlert() {
  let alerta = document.getElementById("alerta");

  if (!alerta) {
    alerta = document.createElement("div");
    alerta.id = "alerta";
    document.body.insertBefore(alerta, document.body.firstChild);
  }

  window.exibirMensagem = function (mensagem, sucesso = false) {
    alerta.textContent = mensagem;
    alerta.style.display = "block";
    alerta.style.backgroundColor = sucesso ? "#d4edda" : "#f8d7da";
    alerta.style.color = sucesso ? "#155724" : "#721c24";

    setTimeout(() => {
      alerta.style.display = "none";
    }, 4000);
  };
}