from typing import List
from lib.service_error_handler import service_error_handler
from .generic_service import GenericService
from lib.hash_fns import decrypt_message, encrypt_message
from database.message_model import Message
from database.user_model import User
from database.chatroom_model import Chatroom
from redis_om import NotFoundError

class MessageService(GenericService):
    def __init__(self) -> None:

        def message_formatter(message: Message):
            msg_dict = message.dict()
            msg_dict["message"] = decrypt_message(msg_dict["message"])
            return msg_dict

        super().__init__(model=Message, formatter=message_formatter)

    def create_message(self, chatroom_pk, sender_pk, message):
        try:
            chatroom = Chatroom.get(chatroom_pk)
            if chatroom.user_pk_1 != sender_pk and chatroom.user_pk_2 != sender_pk:
                raise Exception("You don't belong in that conversation.")
            sender = User.get(sender_pk)
            new_message = self.Model(
                message=encrypt_message(message),
                chatroom_pk=chatroom.pk,
                sender_pk=sender.pk
            )
            new_message.save()
            return (self.format_model(new_message), None)
        except NotFoundError:
            return (None, "User or chatroom not exists")
        except Exception as exc:
            return (None, str(exc))

    @service_error_handler
    def get_messages_of_chatroom(self, chatroom_pk, user_pk, skip: int = 0, limit = 20):
        try:
            chatroom: Chatroom = Chatroom.get(chatroom_pk)
            if chatroom.user_pk_1 == user_pk or chatroom.user_pk_2 == user_pk:
                messages = self.Model.find(self.Model.chatroom_pk == chatroom.pk).sort_by("-created_at").all()
                return ([self.format_model(message) for message in messages[skip:limit]], None)
            else:
                raise Exception("You don't belong in that conversation.")
        except NotFoundError:
            return (None, "Chatroom not found")

    
