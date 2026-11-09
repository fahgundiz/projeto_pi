const form = document.getElementById("loginForm");
const emailInput = document.getElementById("email");
const passInput = document.getElementById("password");
const togglePass = document.getElementById("togglePass");
const formError = document.getElementById("formError");
const submitBtn = document.getElementById("submitBtn");

// ---------- Mostrar / ocultar senha ----------
togglePass.addEventListener("click", () => {
  const show = passInput.type === "password";
  passInput.type = show ? "text" : "password";
  togglePass.textContent = show ? "Ocultar" : "Mostrar";
  togglePass.setAttribute("aria-label", show ? "Ocultar senha" : "Mostrar senha");
});

// ---------- Validação ----------
function setError(input, errorId, message) {
  document.getElementById(errorId).textContent = message;
  input.closest(".field").classList.toggle("has-error", Boolean(message));
  return !message;
}

function validate() {
  const email = emailInput.value.trim();
  const pass = passInput.value;

  const emailOk = setError(
    emailInput, "emailError",
    !email ? "Digite seu e-mail."
    : !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? "Use um e-mail válido, como voce@email.com."
    : ""
  );
  const passOk = setError(
    passInput, "passwordError",
    !pass ? "Digite sua senha."
    : pass.length < 6 ? "A senha precisa ter pelo menos 6 caracteres."
    : ""
  );
  return emailOk && passOk;
}

[emailInput, passInput].forEach(i =>
  i.addEventListener("input", () => { formError.textContent = ""; })
);

// ---------- Envio ----------
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  formError.textContent = "";
  if (!validate()) return;

  submitBtn.disabled = true;
  submitBtn.textContent = "Entrando...";

  try {
    // TODO: troque este trecho pela chamada real ao seu servidor
    await new Promise(r => setTimeout(r, 800));
    window.location.href = "index.html";
  } catch (err) {
    formError.textContent = "Não foi possível entrar. Tente de novo.";
    submitBtn.disabled = false;
    submitBtn.textContent = "Entrar";
  }
});