
class AuditoriaRepository:
    def __init__(self, banco):
        self.banco = banco

    def registrar_auditoria(self, usuario_id, acao, entidade, entidade_id = None, descricao = None, ip = None):
        sql = """
            INSERT INTO auditoria (usuario_id, acao, entidade, entidade_id, ip)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (usuario_id, acao, entidade, entidade_id, descricao, ip)
        self.banco.executar(sql, valores)

    def listar_auditoria(self, usuario_id = None, acao = None, entidade = None):
        sql = """
            SELECT 

                a.id, 
                a.usuario_id,
                a.acao,
                entidade,
                entidade_id,
                descricao,
                ip,
                data_hora,
                u.email,
                u.usuario

            FROM auditoria a

            LEFT JOIN usuarios u
                ON u.id = a.usuario_id

            WHERE 1 = 1
        """
        parametros = []

        if usuario_id:
            sql += """
                AND usuario_id = %s
            """
            parametros.append(f"{usuario_id}")

        if acao:
            sql += """
                AND acao = %s
            """
            parametros.append(f"{acao}")

        if entidade:
            sql += """
                AND entidade = %s
            """
            parametros.append(f"{entidade}")

        sql += " ORDER BY id"

        return self.banco.consultar(sql, tuple(parametros))