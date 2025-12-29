from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.services import GetUserById
from app.lib.database import get_session
from app.exceptions import UserNotFoundException


class SetCurrentUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.current_user = None
        sid = request.cookies.get("sid")
        if sid:
            session_gen = get_session()
            session = next(session_gen)
            try:
                get_user_service = GetUserById(session)
                user = get_user_service.execute(sid)
                request.state.current_user = user
            except UserNotFoundException:
                request.state.current_user = None
            except Exception:
                request.state.current_user = None
            finally:
                session.close()
                try:
                    next(session_gen)
                except StopIteration:
                    pass
        response = await call_next(request)
        return response
