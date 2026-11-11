const form       = document.getElementById('form-login');
const campoEmail = document.getElementById('email');
const campoSenha = document.getElementById('senha');
const erroEmail  = document.getElementById('erro-email');
const erroSenha  = document.getElementById('erro-senha');
const botao      = document.getElementById('btn-entrar');
const textoBotao = botao.querySelector('.btn-texto');
const verSenha   = document.getElementById('ver-senha');
const lembrar    = document.getElementById('lembrar');

/* ---------- Mostrar / esconder senha ---------- */
verSenha.addEventListener('click', () => {
  const visivel = campoSenha.type === 'text';
  campoSenha.type = visivel ? 'password' : 'text';
  verSenha.setAttribute('aria-pressed', String(!visivel));
  verSenha.setAttribute('aria-label', visivel ? 'Mostrar senha' : 'Esconder senha');
  verSenha.textContent = visivel ? '👁️' : '🙈';
});

/* ---------- Validação ---------- */
function mostrarErro(campo, elementoErro, mensagem) {
  campo.setAttribute('aria-invalid', 'true');
  elementoErro.textContent = mensagem;
}

function limparErro(campo, elementoErro) {
  campo.removeAttribute('aria-invalid');
  elementoErro.textContent = '';
}

function validarEmail() {
  const valor = campoEmail.value.trim();
  if (!valor) {
    mostrarErro(campoEmail, erroEmail, 'Digite seu e-mail.');
    return false;
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(valor)) {
    mostrarErro(campoEmail, erroEmail, 'Esse e-mail parece incompleto. Exemplo: nome@exemplo.com');
    return false;
  }
  limparErro(campoEmail, erroEmail);
  return true;
}

function validarSenha() {
  const valor = campoSenha.value;
  if (!valor) {
    mostrarErro(campoSenha, erroSenha, 'Digite sua senha.');
    return false;
  }
  limparErro(campoSenha, erroSenha);
  return true;
}

campoEmail.addEventListener('blur', validarEmail);
campoSenha.addEventListener('blur', validarSenha);
campoEmail.addEventListener('input', () => {
  if (campoEmail.hasAttribute('aria-invalid')) validarEmail();
});
campoSenha.addEventListener('input', () => {
  if (campoSenha.hasAttribute('aria-invalid')) validarSenha();
});

/* ---------- Estado de carregamento ---------- */
function carregando(ativo) {
  botao.disabled = ativo;
  botao.classList.toggle('is-carregando', ativo);
  textoBotao.textContent = ativo ? 'Entrando...' : 'Entrar';
}

/* ---------- Envio ---------- */
form.addEventListener('submit', (evento) => {
  const emailOk = validarEmail();
  const senhaOk = validarSenha();

  // Se algo estiver errado, cancela o envio e leva o foco ao campo com problema
  if (!emailOk || !senhaOk) {
    evento.preventDefault();
    (!emailOk ? campoEmail : campoSenha).focus();
    return;
  }

  // Tudo certo: NÃO chamamos preventDefault, então o navegador envia para o Flask
  if (lembrar.checked) {
    localStorage.setItem('emailLembrado', campoEmail.value.trim());
  } else {
    localStorage.removeItem('emailLembrado');
  }
  carregando(true);
});

/* Se a pessoa voltar para esta página (botão "voltar"), o botão não pode ficar travado */
window.addEventListener('pageshow', () => carregando(false));

/* ---------- Preencher o e-mail lembrado ---------- */
const emailSalvo = localStorage.getItem('emailLembrado');
if (emailSalvo && !campoEmail.value) {
  campoEmail.value = emailSalvo;
  lembrar.checked = true;
}