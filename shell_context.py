from app.services.get_user import GetUser, GetUserService
from app.services.get_user_by_id import GetUserById
from app.repositories.unit_of_work import UnitOfWork, get_unit_of_work
from app.repositories.user_repository import UserRepository
from app.lib.database import get_session
from app.models import User

print("Contesto pronto! Esempi:")
print("  session = next(get_session())")
print("  uow = UnitOfWork(session)")
print("  user_repo = UserRepository(session)")
print("  get_user = GetUser(session)")
print("  get_user_by_id = GetUserById(session)")
