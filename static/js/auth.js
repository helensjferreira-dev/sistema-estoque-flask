document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const alerta = document.getElementById("alerta");

  if (!form || !alerta) return;

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
      const sucesso = retorno.Resultado === true;

      // 🔥 usa o padrão novo
      alerta.className = sucesso ? "alert-success" : "alert-error";
      alerta.textContent = retorno.Mensagem || "Erro no login";
      alerta.style.display = "block";

      if (sucesso) {
        setTimeout(() => (window.location.href = "/"), 1500);
      } else {
        form.reset();
      }
    } catch (error) {
      alerta.className = "alert-error";
      alerta.textContent = "Erro ao conectar com o servidor.";
      alerta.style.display = "block";
    }
  });
});
