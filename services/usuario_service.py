import bcrypt

class UsuarioService():
    def __init__(self, repository):
        self.repository = repository

    def buscar_usuario_pelo_email(self, email):
        if not email:
            raise ValueError("E-mail do usuário é obrigatório")

        usuario = self.repository.buscar_usuario_pelo_email(email)

        return usuario

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
        print(f"Senha em bytes: {senha_bytes}")
        print(f"Hash em bytes: {hash_bytes}")
        print(f"Hash texto: {hash_texto}")


        return hash_texto


