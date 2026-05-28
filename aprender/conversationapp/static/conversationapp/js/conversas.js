document.addEventListener("DOMContentLoaded", () => {
  const painelConversa = document.querySelector(".painel-conversa");
  const userId = Number(painelConversa?.dataset.userId || 0);

  const botoesGrupo = [...document.querySelectorAll(".botao-grupo")];
  const btnToggleGrupos = document.getElementById("btn-toggle-grupos");
  const tituloGrupo = document.getElementById("titulo-grupo");
  const statusConexao = document.getElementById("status-conexao");
  const listaMensagens = document.getElementById("lista-mensagens");

  const formMensagem = document.getElementById("form-mensagem");
  const inputMensagem = document.getElementById("input-mensagem");
  const btnEnviar = document.getElementById("btn-enviar");
  const csrfTokenInput = formMensagem?.querySelector("input[name='csrfmiddlewaretoken']");

  let socket = null;
  let grupoAtualId = null;

  function atualizarEstadoBotaoGrupos() {
    if (!btnToggleGrupos) {
      return;
    }

    const gruposOcultos = document.body.classList.contains("grupos-ocultos");
    btnToggleGrupos.setAttribute("aria-expanded", (!gruposOcultos).toString());
    btnToggleGrupos.setAttribute(
      "aria-label",
      gruposOcultos ? "Mostrar grupos" : "Ocultar grupos"
    );
  }

  function atualizarStatus(texto) {
    if (statusConexao) {
      statusConexao.textContent = texto;
    }
  }

  function habilitarComposer(habilitado) {
    if (!inputMensagem || !btnEnviar) {
      return;
    }

    inputMensagem.disabled = !habilitado;
    btnEnviar.disabled = !habilitado;
    inputMensagem.placeholder = habilitado
      ? "Digite sua mensagem"
      : "Selecione um grupo primeiro";
  }

  function limparMensagens() {
    if (listaMensagens) {
      listaMensagens.innerHTML = "";
    }
  }

  function mostrarMensagemSistema(texto) {
    if (!listaMensagens) {
      return;
    }

    const p = document.createElement("p");
    p.className = "mensagem-sistema";
    p.textContent = texto;
    listaMensagens.appendChild(p);
  }

  function rolarMensagensParaFim() {
    if (listaMensagens) {
      listaMensagens.scrollTop = listaMensagens.scrollHeight;
    }
  }

  function renderMensagem(mensagem) {
    if (!listaMensagens) {
      return;
    }

    const avisos = listaMensagens.querySelectorAll(".mensagem-sistema");
    avisos.forEach((aviso) => aviso.remove());

    const item = document.createElement("article");
    item.className = "mensagem";

    if (Number(mensagem.autor_id) === userId) {
      item.classList.add("minha");
    }

    const texto = document.createElement("p");
    texto.className = "mensagem-texto";
    texto.textContent = mensagem.conteudo;

    const meta = document.createElement("p");
    meta.className = "mensagem-meta";
    meta.textContent = `${mensagem.autor} - ${mensagem.created_at}`;

    item.appendChild(texto);
    item.appendChild(meta);
    listaMensagens.appendChild(item);
    rolarMensagensParaFim();
  }

  function fecharSocketAtual() {
    if (socket) {
      socket.close();
      socket = null;
    }
  }

  function obterCsrfToken() {
    if (csrfTokenInput?.value) {
      return csrfTokenInput.value;
    }

    const cookie = document.cookie
      .split(";")
      .map((item) => item.trim())
      .find((item) => item.startsWith("csrftoken="));
    return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
  }

  function abrirSocketGrupo(grupoId) {
    fecharSocketAtual();

    const protocolo = window.location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = `${protocolo}://${window.location.host}/ws/grupos/${grupoId}/`;

    socket = new WebSocket(wsUrl);

    socket.addEventListener("open", () => {
      atualizarStatus("Conectado em tempo real");
    });

    socket.addEventListener("message", (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.tipo === "nova_mensagem" && data.mensagem) {
          renderMensagem(data.mensagem);
        }
      } catch (erro) {
        console.error("Erro ao ler mensagem do socket:", erro);
      }
    });

    socket.addEventListener("close", () => {
      atualizarStatus("Conexao encerrada");
    });

    socket.addEventListener("error", () => {
      atualizarStatus("Erro de conexao");
    });
  }

  async function carregarHistoricoGrupo(grupoId, nomeGrupo) {
    grupoAtualId = grupoId;
    habilitarComposer(true);

    if (tituloGrupo) {
      tituloGrupo.textContent = nomeGrupo;
    }

    limparMensagens();
    atualizarStatus("Carregando historico...");

    try {
      const response = await fetch(`/conversas/grupos/${grupoId}/mensagens/`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      const mensagens = data.mensagens || [];

      if (mensagens.length === 0) {
        mostrarMensagemSistema("Ainda nao ha mensagens neste grupo.");
      } else {
        mensagens.forEach(renderMensagem);
      }

      abrirSocketGrupo(grupoId);
    } catch (erro) {
      limparMensagens();
      mostrarMensagemSistema("Nao foi possivel carregar as mensagens deste grupo.");
      atualizarStatus("Falha ao carregar historico");
      console.error("Erro ao carregar historico:", erro);
    }
  }

  async function enviarMensagemViaHttp(conteudo) {
    if (!grupoAtualId) {
      return;
    }

    const response = await fetch(`/conversas/grupos/${grupoAtualId}/mensagens/`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": obterCsrfToken(),
      },
      body: JSON.stringify({ conteudo }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    if (data.mensagem) {
      renderMensagem(data.mensagem);
    }
  }

  function marcarBotaoAtivo(botaoAtual) {
    botoesGrupo.forEach((botao) => botao.classList.remove("ativo"));
    botaoAtual.classList.add("ativo");
  }

  botoesGrupo.forEach((botao) => {
    botao.addEventListener("click", () => {
      const grupoId = Number(botao.dataset.grupoId);
      const nomeGrupo = botao.dataset.grupoNome || "Grupo";

      if (!grupoId || grupoId === grupoAtualId) {
        return;
      }

      marcarBotaoAtivo(botao);
      carregarHistoricoGrupo(grupoId, nomeGrupo);
    });
  });

  if (formMensagem) {
    formMensagem.addEventListener("submit", async (event) => {
      event.preventDefault();

      if (!inputMensagem) {
        return;
      }

      const conteudo = inputMensagem.value.trim();
      if (!conteudo) {
        return;
      }

      try {
        if (socket && socket.readyState === WebSocket.OPEN) {
          socket.send(JSON.stringify({ conteudo }));
        } else {
          atualizarStatus("Tempo real indisponivel, enviando pelo servidor...");
          await enviarMensagemViaHttp(conteudo);
        }
        inputMensagem.value = "";
        inputMensagem.focus();
      } catch (erro) {
        atualizarStatus("Erro ao enviar mensagem");
        console.error("Erro ao enviar mensagem:", erro);
      }
    });
  }

  if (btnToggleGrupos) {
    atualizarEstadoBotaoGrupos();
    btnToggleGrupos.addEventListener("click", () => {
      document.body.classList.toggle("grupos-ocultos");
      atualizarEstadoBotaoGrupos();
    });
  }

  if (botoesGrupo.length > 0) {
    botoesGrupo[0].click();
  } else {
    habilitarComposer(false);
    atualizarStatus("Voce nao participa de grupos");
  }

  window.addEventListener("beforeunload", () => {
    fecharSocketAtual();
  });
});
