from pydantic import ValidationError

def service_error_handler(func):

    def wrapper_func(*args, **kwargs):

        try:

            return func(*args, **kwargs)

        except ValidationError as verr:
            return (None, f"Error saving the model: {str(verr)}")
        except Exception as exc:
            return (None, str(exc))
            
    return wrapper_func