
#* EXCEPTIONS
class RequiresSignInException(Exception):
    pass

class ServerErrorPageException(Exception):
    def __init__(self, error_type: str, error_msg: str, error_code: int = 500):
        self.error_type = error_type
        self.error_msg = error_msg
        self.error_code = error_code