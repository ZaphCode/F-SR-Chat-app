from lib.service_error_handler import service_error_handler
from lib.hash_fns import hash_password, verify_password
from .generic_service import GenericService
from schemas.signup_schema import SignUpSch

class UserService(GenericService):
    def __init__(self, model) -> None:
        def custom_formater(user):
            user_dict = user.dict()
            del user_dict["password"]
            return user_dict
        super().__init__(model, custom_formater)

    @service_error_handler
    def register(self, user: SignUpSch):
        user_with_that_credentials = self.Model.find( 
                (self.Model.username == user.username) | 
                (self.Model.email == user.email)
            ).all()
        if user_with_that_credentials:
            raise Exception("Credentials Taken")
        new_user = self.Model(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
            age=user.age,
        )
        new_user.save()
        return (self.format_model(new_user), None)

    @service_error_handler
    def login(self, email: str, password: str):
        user = self.Model.find(self.Model.email == email).first()
        if not verify_password(password, user.password):
            raise Exception("Incorrect password")
        return (self.format_model(user), None)

    


