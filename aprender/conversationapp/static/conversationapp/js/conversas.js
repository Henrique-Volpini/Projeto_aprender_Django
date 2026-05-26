document.addEventListener("DOMContentLoaded", () => {
  const BOTAO_CONFIG = {
    textoAoClicar: "ok",
  };

  const statusClique = document.getElementById("status-clique");
  const botoesGrupo = document.querySelectorAll(".botao-grupo");

  if (!statusClique || botoesGrupo.length === 0) {
    return;
  }

  botoesGrupo.forEach((botao) => {
    botao.addEventListener("click", () => {
      botoesGrupo.forEach((b) => b.classList.remove("ativo"));
      botao.classList.add("ativo");
      statusClique.textContent = BOTAO_CONFIG.textoAoClicar;
    });
  });
});
