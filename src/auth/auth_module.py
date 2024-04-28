from nest.core import Module

from src.auth.auth_service import AuthService


@Module(providers=[AuthService], imports=[], exports=[AuthService])
class AuthModule:
    pass
