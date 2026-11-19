import bcrypt

class UsuarioService():
    def __init__(self, repository):
        self.repository = repository

    def buscar_usuario_pelo_email(self, email):
        if not email:
            raise ValueError("E-mail do usuário é obrigatório")

        usuario = self.repository.buscar_usuario_pelo_email(email)

        return usuario

    def existe_exercicio(self, nome):
        if not nome:
            raise ValueError("Digite o nome do exercício")

        nome = nome.strip().capitalize()
        return self.repository.existe_exercicio(nome)
             
    def cadastrar_exercicio(self, nome, grupo_muscular, descricao = None):
        if not nome or not grupo_muscular:
            raise ValueError("Nome e grupo muscular são obrigatórios")

        nome = nome.strip().capitalize()
        grupo_muscular = grupo_muscular.strip().capitalize()

        existe = self.existe_exercicio(nome)

        if existe:
            raise ValueError("O exercício já está cadastrado")

        return self.repository.cadastrar_exercicio(nome, grupo_muscular, descricao)

    def listar_exercicios(self, grupo_muscular = None):
        return self.repository.listar_exercicios(grupo_muscular = grupo_muscular)

    def listar_treinos(self, usuario_id):
        return self.repository.listar_treinos(usuario_id)

    def detalhar_treino(self, treino_id, usuario_id):
        treino = self.repository.buscar_treino(treino_id, usuario_id)
        if not treino:
            raise ValueError("Treino não encontrado")

        exercicios = self.repository.listar_exercicios_do_treino(treino_id)

        return treino, exercicios

    @staticmethod
    def verificar_senha(senha_digitada, senha_banco_hash):
        #Converter a senha_digitada e a senha_banco_hash em bytes
        senha_digitada_bytes = senha_digitada.encode('utf-8')
        senha_banco_bytes = senha_banco_hash.encode('utf-8')

        comparacao_senhas = bcrypt.checkpw(senha_digitada_bytes, senha_banco_bytes)

        return comparacao_senhas

    @staticmethod
    def gerar_hash_senha(senha):
        #Gerar a senha em bytes
        senha_bytes = senha.encode('utf-8')
        #gera o salto da senha
        salt = bcrypt.gensalt(rounds=12)
        #Gerar o hash da senha em bytes
        hash_bytes = bcrypt.hashpw(senha_bytes, salt)
        #Converter os bytes para string e salvar no banco
        hash_texto = hash_bytes.decode('utf-8')



        return hash_texto


