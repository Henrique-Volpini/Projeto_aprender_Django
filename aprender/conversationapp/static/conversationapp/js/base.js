document.addEventListener("DOMContentLoaded", () => {
  const campoUsuario = document.querySelector('input[name="username"]');
  const campoSenha = document.querySelector('input[name="password"]');
  const btnEnviar = document.querySelector('form button[type="submit"]');

  if (!campoUsuario || !campoSenha || !btnEnviar) {
    return;
  }

  btnEnviar.addEventListener("click", () => {
    console.log("Usuario: ", campoUsuario.value);
    console.log("Senha: ", campoSenha.value);
  });
});
