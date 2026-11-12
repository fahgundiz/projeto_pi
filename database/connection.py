from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

load_dotenv()

class Banco:
    def __init__(self):
        try:
            #========= Cria conexao com o banco de dados =========
            conexao = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                port = int(os.getenv("DB_PORT")),
                use_pure = True
            )
            print("Conectou ao servidor!")

            #========= Verifica se o banco existe =========

            #Cria o cursor
            cursor = conexao.cursor()
            #Busca o nome do banco
            nome_banco = os.getenv("DB_NAME")

            #Quantas linhas existem na lista de banco de dados cujo nome é "NOME_BANCO"
            sql = "SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME=%s"
            parametros = (nome_banco,)

            #Verifica se existe um banco de dados com o nome do banco criado
            cursor.execute(sql, parametros)
            #fetchone() busca uma linha ou None -> vem como uma tupla (1,)
            existe_banco = cursor.fetchone()[0]

            #========= Cria o banco se não existe =========
            if existe_banco == 0:
                cursor = conexao.cursor()
                cursor.execute(f"CREATE DATABASE `{nome_banco}`")
                cursor.close()
                print("Banco criado")
            else:
                print("Banco já existia")

            #fecha o cursor
            cursor.close()
            #fecha conexão
            conexao.close()

            #========= Conecta ao banco específico =========
            self.conexao = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                database = nome_banco,
                port = int(os.getenv("DB_PORT")),
                use_pure = True
            )
            
            self.cursor = self.conexao.cursor(dictionary=True)


        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            raise

    def fechar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()

    def executar(self, sql, parametros=None):
        self.cursor.execute(sql, parametros or ())
        self.conexao.commit()

    def consultar(self, sql, parametros=None):
        self.cursor.execute(sql, parametros or ())
        return self.cursor.fetchall()

    def consultar_um(self, sql, parametros=None):
        self.cursor.execute(sql, parametros or ())
        return self.cursor.fetchone()