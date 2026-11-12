from database.connection import Banco

db = Banco()

# consultar a tabela
usuarios = db.consultar("SELECT * FROM usuarios")
print(usuarios)

print("Usuarios select OK")

#consulta um usuario
usuario = db.consultar_um("SELECT * FROM usuarios WHERE email = %s", ("ana@email.com",))
print(f"usuário: {usuario}")
print(f"Nome do usuário: {usuario['nome']}")

db.fechar()
