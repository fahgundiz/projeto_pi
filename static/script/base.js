// ---------- Navegação entre telas ----------
const navButtons = document.querySelectorAll(".nav-btn");
const views = document.querySelectorAll(".view");

function showView(id) {
  views.forEach(v => v.classList.toggle("is-active", v.id === id));
  navButtons.forEach(b => {
    const active = b.dataset.view === id;
    b.classList.toggle("is-active", active);
    if (active) b.setAttribute("aria-current", "page");
    else b.removeAttribute("aria-current");
  });
}

navButtons.forEach(btn =>
  btn.addEventListener("click", () => showView(btn.dataset.view))
);

// ---------- XP, nível e moedas ----------
const state = { xp: 0, level: 1, coins: 0 };
const XP_PER_LEVEL = 100;

const xpFill = document.getElementById("xpFill");
const xpBar = document.querySelector(".xp-bar");
const levelEl = document.getElementById("level");
const coinsEl = document.getElementById("coins");

function render() {
  xpFill.style.width = state.xp + "%";
  xpBar.setAttribute("aria-valuenow", state.xp);
  levelEl.textContent = state.level;
  coinsEl.textContent = state.coins;
}

function addXP(amount) {
  state.xp += amount;
  state.coins += 5;
  while (state.xp >= XP_PER_LEVEL) {
    state.xp -= XP_PER_LEVEL;
    state.level++;
  }
  render();
}

document.getElementById("completeBtn").addEventListener("click", () => addXP(20));

render();