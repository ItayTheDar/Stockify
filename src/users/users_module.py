from src.users.users_controller import UsersController
from src.users.users_service import UsersService
from nest.core import Module

@Module(controllers=[UsersController], providers=[UsersService], imports=[])
class UsersModule:
    pass
