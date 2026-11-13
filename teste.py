from repositories.usuario_repository import UsuarioRepository
from  services.usuario_service import UsuarioService




usuario_service = UsuarioService(UsuarioRepository)

usuario_service.gerar_hash_senha("teste")