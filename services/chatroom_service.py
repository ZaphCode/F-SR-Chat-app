import imp
from pydantic import ValidationError
from lib.service_error_handler import service_error_handler
from .generic_service import GenericService
from database.user_model import User
from database.chatroom_model import Chatroom
from redis_om import NotFoundError

class ChatroomService(GenericService):
    def __init__(self) -> None:
        super().__init__(model=Chatroom)

    def get_chatroom_if_exist(self, user_pk_1, user_pk_2):
        try:
            chatroom: Chatroom = self.Model.find(
                ((self.Model.user_pk_1 == user_pk_1) & 
                (self.Model.user_pk_2 == user_pk_2)) | 
                ((self.Model.user_pk_1 == user_pk_2) & 
                (self.Model.user_pk_2 == user_pk_1))).first()
            return self.format_model(chatroom)
        except NotFoundError:
            return None

    def create_or_get_chatroom(self, user_pk_1, user_pk_2):
        try:
            user_1: User = User.get(user_pk_1)
            user_2: User = User.get(user_pk_2)
            chatroom = self.get_chatroom_if_exist(user_pk_1=user_1.pk, user_pk_2=user_2.pk)
            if chatroom:
                print("Already exists")
                return (self.format_model(chatroom), None)
            new_chatroom = self.Model(
                user_pk_1 = user_1.pk,
                user_pk_2=user_2.pk
            )
            print("New created")
            new_chatroom.save()
            return (self.format_model(new_chatroom), None)
        except NotFoundError:
            return (None, "User o User' not found")
        except ValidationError:
            return (None, "Error validating")

            
        

        
