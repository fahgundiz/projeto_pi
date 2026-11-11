const botoes = document.querySelectorAll('.nav-btn');
const telas = document.querySelectorAll('.view');

// Percore todos os 3 botoes do nav
botoes.forEach(botao => {
  //Para cada botao, espere um clique
  botao.addEventListener('click', () =>{
    //Quando um botao for clicado, desativa todos
    botoes.forEach(b =>{
      b.classList.remove('ativo');
      b.removeAttribute('aria-current')
    })
    //Desativa todas as telas
    telas.forEach(t => {
      t.classList.remove('ativo')
    })

    //Pinta o botao selecionado de 'roxo'
    botao.classList.add('ativo');
    //avisa o leitor de tela da pagina atual
    botao.setAttribute('aria-current','pagina_ativa');

    //busca o id da página(section: habitos, progresso e hoje) clicada
    const idDaTela = botao.dataset.view;
    //entra a section clicada e adiciona ativo fazendo ela aparecer
    document.getElementById(idDaTela).classList.add('ativo')
  })

  

})