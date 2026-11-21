
class UsuarioRepository:
    def __init__(self, banco):
        self.banco = banco

    def buscar_usuario_pelo_email(self, email):
        """
        Busca um usuário pelo email dele e retorna o usuário.
        """
        sql = """
            SELECT id, usuario, email, senha, data_nascimento, perfil
            FROM usuarios
            WHERE email = %s
"""
        usuario = self.banco.consultar_um(sql, (email,))

        return usuario

    def existe_exercicio(self, nome):
        sql = "SELECT id FROM exercicios WHERE nome = %s"
        existe = self.banco.consultar_um(sql, (nome,))
        return existe
    
    def cadastrar_exercicio(self, nome, grupo_muscular, descricao = None):
        """
        Cadastra um exercício na tabela exercicios e devolve seu ID.
        """
        sql = """
            INSERT INTO exercicios (nome, grupo_muscular, descricao)
            VALUES (%s, %s, %s)
"""
        return self.banco.executar(sql, (nome, grupo_muscular, descricao))

    def listar_exercicios(self, grupo_muscular = None):
        sql = """
            SELECT
                id,
                nome,
                grupo_muscular,
                descricao

            FROM exercicios
            WHERE 1 = 1
        """

        parametros = []

        if grupo_muscular:
            sql += """
                AND grupo_muscular LIKE %s
            """
            parametros.append(f"%{grupo_muscular}%")

        sql += """ ORDER BY nome"""

        return self.banco.consultar(sql, tuple(parametros))

    def listar_treinos(self, usuario_id):
        sql = """
            SELECT 
                t.id,
                t.nome,
                t.descricao,
                t.criado_em,
                COUNT(te.id) AS total_exercicios

            FROM treinos t    
            
            LEFT JOIN treino_exercicios te
                ON te.treino_id = t.id

            WHERE t.usuario_id = %s

            GROUP BY t.id, t.nome, t.descricao, t.criado_em
            ORDER BY t.criado_em DESC
"""
        return self.banco.consultar(sql, (usuario_id,))

    def buscar_treino(self, treino_id, usuario_id):
        sql = """
            SELECT 
                id,
                nome,
                descricao,
                criado_em

            FROM treinos
            WHERE id = %s and usuario_id = %s
"""
        return self.banco.consultar_um(sql, (treino_id, usuario_id))

    def listar_exercicios_do_treino(self, treino_id):
        sql = """
            SELECT
                te.ordem,
                e.nome,
                e.grupo_muscular,
                te.series,
                te.repeticoes,
                te.carga_kg,
                te.descanso_seg
                
            
            FROM treino_exercicios te

            JOIN exercicios e 
                ON e.id = te.exercicio_id
            
            WHERE te.treino_id = %s
            ORDER BY te.ordem
"""
        return self.banco.consultar(sql, (treino_id,))

    def criar_treino_completo(self, usuario_id, nome, descricao, itens):
        """Itens: lista de dicionario com exercicio_id, series, repeticoes, carga_kg, descanso_seg"""
        try:
            #Cria o treino
            treino_id = self.banco.executar_sem_commit(
                "INSERT INTO treinos (usuario_id, nome, descricao) VALUES (%s, %s, %s)", (usuario_id, nome, descricao)
            )

            #Insere os "itens"
            for ordem, item in enumerate(itens, start=1):
                self.banco.executar_sem_commit(
                    """
                        INSERT INTO treino_exercicios
                        (treino_id, exercicio_id, series, repeticoes, carga_kg, descanso_seg, ordem)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (treino_id, item["exercicio_id"], item["series"], item["repeticoes"], item["carga_kg"], item["descanso_seg"], ordem)
                )

            self.banco.confirmar()
            return treino_id


        except Exception:
            self.banco.desfazer()
            raise