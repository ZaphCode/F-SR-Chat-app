from pydantic import ValidationError
from lib.service_error_handler import service_error_handler
from .generic_service import GenericService
from database.user_model import User
from database.chatroom_model import Chatroom
from .user_service import UserService
from redis_om import NotFoundError

user_service = UserService()

class ChatroomService(GenericService):
    def __init__(self) -> None:

        def chatroom_formatter(chatroom: Chatroom):
             user_1, err = user_service.get_by_pk(chatroom.user_pk_1)
             user_2, err2 = user_service.get_by_pk(chatroom.user_pk_2)
             chatroom_dict = chatroom.dict()
             chatroom_dict["user_1_populated"] = user_1
             chatroom_dict["user_2_populated"] = user_2
             return chatroom_dict

        super().__init__(model=Chatroom, formatter=chatroom_formatter)

    def get_chatroom_if_exist(self, user_pk_1, user_pk_2):
        try:
            chatroom: Chatroom = self.Model.find(
                ((self.Model.user_pk_1 == user_pk_1) & 
                (self.Model.user_pk_2 == user_pk_2)) | 
                ((self.Model.user_pk_1 == user_pk_2) & 
                (self.Model.user_pk_2 == user_pk_1))).first()
            return chatroom
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

    @service_error_handler
    def get_chatrooms_of_user(self, user_pk):
        chatrooms = self.Model.find(
            (self.Model.user_pk_1 == user_pk) | 
            (self.Model.user_pk_2 == user_pk) 
        ).all()
        return ([self.format_model(chatroom) for chatroom in chatrooms], None)

            
        

        
