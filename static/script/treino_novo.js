const btnAdicionar = document.getElementById("btn-adicionar")
// Cria as variavel linhas pelo JS
const container = document.getElementById("linhas")
// Cria o modelo do  template
const modelo = document.getElementById("modelo-linha")

function adicionarLinha(){
    // content permite acessar o conteúdo interno do template
    // cloneNode faz um cópia exata do conteúdo
    // o parametro true diz para fazer uma clonagem profunda, todos os elementes e atributos  que estiverem dentro
    const linha = modelo.content.cloneNode(true)

    // Busca a classe btn-remover do template modelo-linha
    linha.querySelector(".btn-remover").addEventListener("click", (e)=>{
        // e.target é o elemente exato que foi clicado "botao x"
        // closest sobe na árvore até encontrar o ancestral com a classe "linha-exercicio"
        // remove() apaga esse ancestral
        e.target.closest(".linha-exercicio").remove()
    })
    container.appendChild(linha)
}

// Quando o botao for clicado
btnAdicionar.addEventListener("click", adicionarLinha)

// Quando a página carrega já mostra um exercício para preencher
adicionarLinha()