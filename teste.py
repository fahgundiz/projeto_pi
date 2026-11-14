from database.connection import Banco
from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService



banco = Banco()
usuario_repo = UsuarioRepository(banco)
usuario_service =  UsuarioService(usuario_repo)

print("======= TESTE CONSULTA EXERCÍCIOS SEM PARAMETROS =======")
exercicios = usuario_service.listar_exercicios()
for exercicio in exercicios:
    print(f"Exercício: {exercicio}")

print("======= TESTE CONSULTA EXERCÍCIOS COM PARAMETRO GRUPO MUSCULAR =======")
exercicios = usuario_service.listar_exercicios("peito")
for exercicio in exercicios:
    print(f"Exercício: {exercicio}")
