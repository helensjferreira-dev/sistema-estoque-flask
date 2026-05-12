document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const alerta = document.getElementById("alerta");

  if (!form || !alerta) return;

  function mostrarAlerta(mensagem, sucesso = false) {
    alerta.classList.remove("alert-success", "alert-error");
    alerta.classList.add(sucesso ? "alert-success" : "alert-error");
    alerta.textContent = mensagem;
    alerta.style.display = "block";
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value.trim();

    try {
      const resposta = await fetch("/usuario/logon", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
      });

      const retorno = await resposta.json();
      const sucesso =
  retorno.Resultado === true ||
  retorno.Resultado === "true";

      mostrarAlerta(retorno.Mensagem || "Erro no login.", sucesso);

      if (sucesso) {
        setTimeout(() => {
          window.location.href = "/";
        }, 1000);
      } else {
        form.reset();
      }
    } catch (error) {
      console.error("Erro no login:", error);
      mostrarAlerta("Erro ao conectar com o servidor.", false);
    }
  });
});