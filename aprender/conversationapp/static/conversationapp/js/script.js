const campo1 = document.getElementById("campo1");
const campo2 = document.getElementById("campo2");
const btnEnviar = document.getElementById("btnEnviar");

btnEnviar.addEventListener("click", () => {
  const valorCampo1 = campo1.value;
  const valorCampo2 = campo2.value;

  console.log("Usuário: ", valorCampo1);
  console.log("Senha: ", valorCampo2);
});