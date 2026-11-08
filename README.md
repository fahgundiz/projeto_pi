# 💪 APP de Treino (nome ainda a pensar)

Aplicativo web para **organizar treinos de musculação**, com cadastro de exercícios, controle de cargas e criação de planilhas de treino personalizadas.

## Descrição

O projeto permite que o usuário monte suas rotinas de treino, registre a evolução das cargas em cada exercício e acompanhe seu progresso ao longo do tempo.

Também tem como objetivo demonstrar boas práticas de desenvolvimento: organização em módulos (padrão MVC), uso de Git e estrutura de projeto escalável com Flask.

## Funcionalidades

- [x] Página inicial
- [ ] Cadastro de exercícios (nome, grupo muscular, descrição)
- [ ] Registro de cargas, séries e repetições
- [ ] Histórico de evolução de carga por exercício
- [ ] Criação e edição de planilhas de treino (ex.: Treino A/B/C)
- [ ] Associação de exercícios a planilhas
- [ ] Gráficos de progresso
- [ ] Autenticação de usuários

## Estrutura do Projeto

```
01_Flask_HTML/
├── controllers/
│   ├── base_controller.py        # Classe base que registra as rotas no Flask
│   └── html_base_controller.py   # Controller das páginas HTML
├── templates/                    # Arquivos HTML (Jinja2)
├── static/                       # CSS, JavaScript e imagens
├── app.py                        # Ponto de entrada da aplicação
├── requirements.txt              # Dependências do projeto
├── .env                          # Variáveis de ambiente (não versionado)
├── .gitignore
├── LICENSE
└── README.md
```

### Como funciona a arquitetura

Cada controller herda de `BaseController` e define uma lista `rotas` com tuplas no formato `(url, nome_do_endpoint, função)`. O `BaseController` percorre essa lista e registra cada rota no Flask automaticamente, evitando repetição de `@app.route` pelo código.

## Pré-requisitos

- Python >= 3.10
- pip
- venv

## Instalação

### Clonando o repositório

```bash
git clone https://github.com/usuario/repositorio.git
cd repositorio
```

### Criando e ativando o ambiente virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python -m venv venv
source venv/bin/activate
```

### Instalando as dependências

```bash
pip install -r requirements.txt
```

### Configurando variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta
```

> O arquivo `.env` não deve ser enviado ao repositório. Confirme que ele está no `.gitignore`.

## Execução

```bash
python app.py
```

Acesse no navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Testes

Executar os testes automatizados:

```bash
pytest
```

Recomenda-se manter os testes na pasta `tests/`.

## Branches

- `main`: versão estável do projeto
- `dev`: desenvolvimento de novas funcionalidades

## Tecnologias e Dependências

- Python 3.x
- Flask
- HTML5 / CSS3
- Jinja2 (templates)
- python-dotenv (variáveis de ambiente)

## Licença

Distribuído sob a licença descrita no arquivo [LICENSE](LICENSE).

## Autor / Contato

- Nome do autor: Gabriel Fagundes 
- GitHub: https://github.com/fahgundiz
- E-mail: gabrielfagundesespinoza@hotmail.com