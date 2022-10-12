from fastapi import Request, WebSocket, status
from services.user_service import UserService
from lib.exceptions import RequiresSignInException, ServerErrorPageException

user_service = UserService()

def get_user_required(request: Request):
    user_pk = request.session.get("user_pk")
    if not user_pk:
        raise RequiresSignInException()
    user, error = user_service.get_by_pk(user_pk)
    if error or not user:
        request.session.pop("user_pk", None)
        raise ServerErrorPageException("Auth", "Something wear happend")
    return user

def get_user_optional(request: Request):
    user_pk = request.session.get("user_pk")
    if not user_pk:
        return None
    user, error = user_service.get_by_pk(user_pk)
    if error or not user:
        request.session.pop("user_pk", None)
        raise ServerErrorPageException("SERVER-ERROR", "Something wear happend") 
    return user

def get_user_ws(websocket: WebSocket):
    user_pk = websocket.session.get("user_pk")
    if not user_pk:
        websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    user, error = user_service.get_by_pk(user_pk)
    if error:
        raise ServerErrorPageException("SERVER-ERROR", "Something wear happend")
    return user